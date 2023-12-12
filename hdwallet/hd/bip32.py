#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from __future__ import annotations

from typing import Optional, Type, Union, Tuple, List
from hashlib import sha256

import hmac
import hashlib
import struct

from ..libs.ripemd160 import ripemd160
from ..libs.base58 import (
    check_encode, checksum_encode, check_decode, ensure_string
)
from ..ecc import (
    IPoint, IPublicKey, IPrivateKey, EllipticCurveCryptography,
    KholawEd25519, KholawEd25519Point, KholawEd25519PublicKey, KholawEd25519PrivateKey,
    SLIP10Ed25519, SLIP10Ed25519Point, SLIP10Ed25519PublicKey, SLIP10Ed25519PrivateKey,
    SLIP10Ed25519Blake2b, SLIP10Ed25519Blake2bPoint, SLIP10Ed25519Blake2bPublicKey, SLIP10Ed25519Blake2bPrivateKey,
    SLIP10Nist256p1, SLIP10Nist256p1Point, SLIP10Nist256p1PublicKey, SLIP10Nist256p1PrivateKey,
    SLIP10Secp256k1, SLIP10Secp256k1Point, SLIP10Secp256k1PublicKey, SLIP10Secp256k1PrivateKey
)
from ..derivations import IDerivation
from ..addresses.p2pkh import P2PKHAddress
from ..wif import (
    private_key_to_wif, wif_to_private_key
)
from ..crypto import hmac_sha512
from ..utils import (
    get_bytes, bytes_to_integer, integer_to_bytes, bytes_to_string, reset_bits, set_bits
)
from .ihd import IHD


FINGERPRINT_MASTER_KEY: bytes = b"\x00\x00\x00\x00"
PRIVATE_KEY_PREFIX: bytes = b"\x00"


class BIP32(IHD):

    _ecc: EllipticCurveCryptography

    _seed: Optional[bytes] = None
    _hmac: Optional[bytes] = None

    _root_private_key: Optional[IPrivateKey] = None
    _private_key: Optional[IPrivateKey] = None
    _root_public_key: Optional[IPublicKey] = None
    _public_key: Optional[IPublicKey] = None
    _root_chain_code: Optional[bytes] = None
    _chain_code: Optional[bytes] = None

    _wif_type: str
    _public_key_type: str

    _path: str = "m/"
    _indexes: List[int] = []
    _fingerprint: Optional[bytes] = None
    _parent_fingerprint: Optional[bytes] = None
    _root_depth: int = 0
    _depth: int = 0
    _root_index: int = 0
    _index: int = 0

    def name(self) -> str:
        return "BIP32"

    def __init__(self, ecc_name: str, public_key_type: str = "compressed"):

        self._ecc_name: str = ecc_name
        self._ecc: EllipticCurveCryptography = self.get_ecc(
            ecc_name=ecc_name
        )
        if public_key_type == "uncompressed":
            self._wif_type = "wif"
        elif public_key_type == "compressed":
            self._wif_type = "wif-compressed"
        else:
            raise ValueError(f"Invalid Electrum v1 public key type, (expected: 'uncompressed' or 'compressed' types, got: '{public_key_type}')")
        self._public_key_type = public_key_type

    @staticmethod
    def get_hmac(ecc_name: str) -> bytes:
        ecc_name_upper: str = ecc_name.upper()
        if ecc_name_upper in [
            "KHOLAW-ED25519", "SLIP10-ED25519", "SLIP10-ED25519-BLAKE2B"
        ]:
            return b"ed25519 seed"
        elif ecc_name_upper == "SLIP10-NIST256P1":
            return b"Nist256p1 seed"
        elif ecc_name_upper == "SLIP10-SECP256K1":
            return b"Bitcoin seed"
        else:
            raise ValueError("Invalid curve type")

    @staticmethod
    def get_ecc(ecc_name: str) -> EllipticCurveCryptography:
        ecc_name_upper: str = ecc_name.upper()
        if ecc_name_upper == "KHOLAW-ED25519":
            return KholawEd25519
        elif ecc_name_upper == "SLIP10-ED25519":
            return SLIP10Ed25519
        elif ecc_name_upper == "SLIP10-ED25519-BLAKE2B":
            return SLIP10Ed25519Blake2b
        elif ecc_name_upper == "SLIP10-NIST256P1":
            return SLIP10Nist256p1
        elif ecc_name_upper == "SLIP10-SECP256K1":
            return SLIP10Secp256k1
        else:
            raise ValueError("Invalid curve type")

    def from_seed(self, seed: Union[bytes, str], **kwargs) -> BIP32:

        self._seed = get_bytes(seed)
        if len(self._seed) < 16:
            raise ValueError(f"Invalid seed length ({len(self._seed)})")

        hmac_half_length: int = hashlib.sha512().digest_size // 2

        # Compute HMAC, retry if the resulting private key is not valid
        self._hmac: bytes = b""
        hmac_data: bytes = self._seed
        success: bool = False

        while not success:
            self._hmac = hmac.digest(
                self.get_hmac(ecc_name=self._ecc_name), hmac_data, "sha512"
            ) if hasattr(hmac, "digest") else hmac.new(
                self.get_hmac(ecc_name=self._ecc_name), hmac_data, hashlib.sha512
            ).digest()

            if self._ecc.curve_name() == "Kholaw-Ed25519":
                # Compute kL and kR
                success = ((self._hmac[:hmac_half_length][31] & 0x20) == 0)
                if not success:
                    hmac_data = self._hmac
            else:
                private_key_class: IPrivateKey = self._ecc.private_key_class()
                # If private key is not valid, the new HMAC data is the current HMAC
                success = private_key_class.is_valid_bytes(self._hmac[:hmac_half_length])
                if not success:
                    hmac_data = self._hmac

        def tweak_master_key_bits(data: bytes) -> bytes:

            data: bytearray = bytearray(data)
            # Clear the lowest 3 bits of the first byte of kL
            data[0] = reset_bits(data[0], 0x07)
            # Clear the highest bit of the last byte of kL
            data[31] = reset_bits(data[31], 0x80)
            # Set the second-highest bit of the last byte of kL
            data[31] = set_bits(data[31], 0x40)

            return bytes(data)

        if self._ecc.curve_name() == "Kholaw-Ed25519":
            # Compute kL and kR
            kl_bytes, kr_bytes = (
                self._hmac[:hmac_half_length], self._hmac[hmac_half_length:]
            )
            # Tweak kL bytes
            kl_bytes = tweak_master_key_bits(kl_bytes)

            chain_code_bytes = hmac.digest(
                self.get_hmac(ecc_name=self._ecc_name), b"\x01" + self._seed, "sha256"
            ) if hasattr(hmac, "digest") else hmac.new(
                self.get_hmac(ecc_name=self._ecc_name), b"\x01" + self._seed, hashlib.sha256
            ).digest()

            self._root_private_key, self._root_chain_code = (
                self._ecc.private_key_class().from_bytes(
                    (kl_bytes + kr_bytes)
                ), chain_code_bytes
            )
        else:
            self._root_private_key, self._root_chain_code = (
                self._ecc.private_key_class().from_bytes(
                    self._hmac[:hmac_half_length]
                ), self._hmac[hmac_half_length:]
            )

        self._private_key, self._chain_code, self._parent_fingerprint = (
            self._root_private_key, self._root_chain_code, FINGERPRINT_MASTER_KEY
        )
        self._root_public_key = self._private_key.public_key()
        self._public_key = self._root_public_key
        return self

    @staticmethod
    def _deserialize_xprivate_key(xprivate_key: str, encoded: bool = True) -> tuple:
        decoded_xprivate_key: str = (
            check_decode(xprivate_key) if encoded else xprivate_key
        )
        if len(decoded_xprivate_key) != 78:  # 156
            raise ValueError("Invalid xprivate key.")
        return (
            decoded_xprivate_key[:4], decoded_xprivate_key[4:5],
            decoded_xprivate_key[5:9], decoded_xprivate_key[9:13],
            decoded_xprivate_key[13:45], decoded_xprivate_key[46:]
        )

    def from_xprivate_key(self, xprivate_key: str, strict: bool = False, encoded: bool = True) -> BIP32:
        # if not is_root_xprivate_key(xprivate_key=xprivate_key, symbol=self._cryptocurrency.SYMBOL):
        #     if strict:
        #         raise ValueError("Invalid root xprivate key.")

        _deserialize_xprivate_key = self._deserialize_xprivate_key(
            xprivate_key=xprivate_key, encoded=encoded
        )
        self._root_depth, self._root_index = (
            int.from_bytes(_deserialize_xprivate_key[1], "big"),
            struct.unpack(">L", _deserialize_xprivate_key[3])[0]
        )
        self._depth, self._fingerprint, self._index = (
            int.from_bytes(_deserialize_xprivate_key[1], "big"),
            _deserialize_xprivate_key[2],
            struct.unpack(">L", _deserialize_xprivate_key[3])[0]
        )
        self._root_private_key, self._root_chain_code = (
            _deserialize_xprivate_key[5], _deserialize_xprivate_key[4]
        )
        self._private_key, self._chain_code, self._parent_fingerprint = (
            self._ecc.private_key_class().from_bytes(
                self._root_private_key
            ),
            self._root_chain_code,
            FINGERPRINT_MASTER_KEY
        )
        self._root_public_key = self._private_key.public_key()
        self._public_key = self._root_public_key
        return self

    # @staticmethod
    # def _deserialize_xpublic_key(xpublic_key: str, encoded: bool = True) -> tuple:
    #     decoded_xpublic_key: str = (
    #         check_decode(xpublic_key) if encoded else xpublic_key
    #     )
    #     if len(decoded_xpublic_key) != 78:  # 156
    #         raise ValueError("Invalid xpublic key.")
    #     return (
    #         decoded_xpublic_key[:4], decoded_xpublic_key[4:5],
    #         decoded_xpublic_key[5:9], decoded_xpublic_key[9:13],
    #         decoded_xpublic_key[13:45], decoded_xpublic_key[45:]
    #     )
    #
    # def from_xpublic_key(self, xpublic_key: str, strict: bool = False, encoded: bool = True) -> BIP32:
    #     # if not is_root_xpublic_key(xpublic_key=xpublic_key, symbol=self._cryptocurrency.SYMBOL):
    #     #     if strict:
    #     #         raise ValueError("Invalid root xpublic key.")
    #
    #     _deserialize_xpublic_key = self._deserialize_xpublic_key(
    #         xpublic_key=xpublic_key, encoded=encoded
    #     )
    #     self._root_depth, self._root_index = (
    #         int.from_bytes(_deserialize_xpublic_key[1], "big"),
    #         struct.unpack(">L", _deserialize_xpublic_key[3])[0]
    #     )
    #     self._depth, self._fingerprint, self._index = (
    #         int.from_bytes(_deserialize_xpublic_key[1], "big"),
    #         _deserialize_xpublic_key[2],
    #         struct.unpack(">L", _deserialize_xpublic_key[3])[0]
    #     )
    #     self._root_public_key, self._root_chain_code = (
    #         _deserialize_xpublic_key[5], _deserialize_xpublic_key[4]
    #     )
    #     self._public_key, self._chain_code, self._parent_fingerprint = (
    #         self._ecc.public_key_class().from_bytes(
    #             self._root_public_key
    #         ),
    #         self._root_chain_code,
    #         FINGERPRINT_MASTER_KEY
    #     )
    #     return self

    def from_wif(self, wif: str) -> BIP32:
        return self.from_private_key(private_key=wif_to_private_key(wif=wif))

    def from_private_key(self, private_key: str) -> BIP32:
        self._private_key = SLIP10Ed25519PrivateKey.from_bytes(get_bytes(private_key))
        self._public_key = self._private_key.public_key()
        return self

    def from_public_key(self, public_key: str) -> BIP32:
        pass

    def from_derivation(self, derivation: IDerivation) -> BIP32:

        if not isinstance(derivation, IDerivation):
            raise ValueError("Invalid derivation class")

        for index in derivation.indexes():
            self._path += ((
                f"{index - 0x80000000}'"
                if self._path == "m/" else
                f"/{index - 0x80000000}'"
            ) if index & 0x80000000 else (
                f"{index}"
                if self._path == "m/" else
                f"/{index}"
            ))
            self._indexes.append(index)
            self.drive(index)
        return self

    def update_derivation(self, derivation: IDerivation) -> BIP32:

        if not isinstance(derivation, IDerivation):
            raise ValueError("Invalid derivation class")

        self.clean_derivation()
        self.from_derivation(
            derivation=derivation
        )
        return self

    def clean_derivation(self) -> BIP32:
        if self._root_private_key:
            self._private_key, self._chain_code, self._parent_fingerprint = (
                self._root_private_key, self._root_chain_code, b"\x00\x00\x00\x00"
            )
            self._public_key = self._private_key.public_key()
            self._indexes = []
            self._path = "m/"
            self._depth = 0
        elif self._root_public_key:
            self._public_key, self._chain_code, self._parent_fingerprint = (
                self._root_public_key, self._root_chain_code, b"\x00\x00\x00\x00"
            )
            self._indexes = []
            self._path = "m/"
            self._depth = 0

        return self

    # def from_path(self, path: str) -> BIP32:
    #
    #     if str(path)[0:2] != "m/":
    #         raise ValueError(f"Bad path, please insert like this type of path \"m/0'/0\"!, not: ({path})")
    #
    #     for index in path.lstrip("m/").split("/"):
    #         if "'" in index:
    #             _index: int = int(index[:-1]) + 0x80000000
    #             self._indexes.append(_index)
    #             self._path += f"/{index}'"
    #             self.drive(_index)
    #         else:
    #             _index: int = int(index)
    #             self._indexes.append(_index)
    #             self._path += f"/{index}"
    #             self.drive(_index)
    #     return self
    #
    # def from_index(self, index: int, hardened: bool = False) -> BIP32:
    #
    #     if not isinstance(index, int):
    #         raise ValueError("Bad index, Please import only integer number!")
    #
    #     if hardened:
    #         _index: int = index + 0x80000000
    #         self._indexes.append(_index)
    #         self._path += f"/{index}"
    #         self.drive(_index)
    #     else:
    #         self._indexes.append(index)
    #         self._path += f"/{index}"
    #         self.drive(index)
    #
    #     return self

    def drive(self, index: int) -> Optional[BIP32]:

        hmac_half_length: int = hashlib.sha512().digest_size // 2

        if self._ecc.name() == "Kholaw-Ed25519":
            index_bytes: bytes = integer_to_bytes(
                data=index, bytes_num=4, endianness="little"
            )
            if self._private_key:
                if index & 0x80000000:
                    if self._private_key is None:
                        raise ValueError("Hardened derivation path is invalid for xpublic key")
                    z_hmac: bytes = hmac_sha512(self._chain_code, (
                        b"\x00" + self._private_key.raw() + index_bytes
                    ))
                    _hmac: bytes = hmac_sha512(self._chain_code, (
                        b"\x01" + self._private_key.raw() + index_bytes
                    ))
                else:
                    z_hmac: bytes = hmac_sha512(self._chain_code, (
                        b"\x02" + self._public_key.raw_compressed()[1:] + index_bytes
                    ))
                    _hmac: bytes = hmac_sha512(self._chain_code, (
                        b"\x03" + self._public_key.raw_compressed()[1:] + index_bytes
                    ))

                def new_private_key_left_part(zl: bytes, kl: bytes, ecc: EllipticCurveCryptography) -> bytes:
                    zl: int = bytes_to_integer(zl[:28], endianness="little")
                    kl: int = bytes_to_integer(kl, endianness="little")

                    private_key_left: int = (zl * 8) + kl
                    # Discard child if multiple of curve order
                    if private_key_left % ecc.order() == 0:
                        raise ValueError("Computed child key is not valid, very unlucky index")

                    return integer_to_bytes(
                        private_key_left, bytes_num=(
                            KholawEd25519PrivateKey.length() // 2
                        ), endianness="little"
                    )

                def new_private_key_right_part(zr: bytes, kr: bytes) -> bytes:
                    zr: int = bytes_to_integer(zr, endianness="little")
                    kr: int = (zr + bytes_to_integer(kr, endianness="little")) % (2 ** 256)

                    return integer_to_bytes(
                        kr, bytes_num=(
                            KholawEd25519PrivateKey.length() // 2
                        ), endianness="little"
                    )

                z_hmacl, z_hmacr, _hmacl, _hmacr = (
                    z_hmac[:hmac_half_length], z_hmac[hmac_half_length:],
                    _hmac[:hmac_half_length], _hmac[hmac_half_length:]
                )

                kl_bytes, kr_bytes = (
                    new_private_key_left_part(
                        zl=z_hmacl, kl=self._private_key.raw()[:hmac_half_length], ecc=self._ecc
                    ), new_private_key_right_part(
                        zr=z_hmacr, kr=self._private_key.raw()[hmac_half_length:]
                    )
                )

                self._private_key, self._chain_code, self._parent_fingerprint = (
                    self._ecc.private_key_class().from_bytes(
                        kl_bytes + kr_bytes
                    ),
                    _hmacr,
                    get_bytes(self.finger_print())
                )
                self._public_key = self._private_key.public_key()
                self._depth, self._index, self._fingerprint = (
                    (self._depth + 1), index, get_bytes(self.finger_print())
                )
            else:
                if index & 0x80000000:
                    raise ValueError("Hardened derivation path is invalid for xpublic key")
                z_hmac: bytes = hmac_sha512(self._chain_code, (
                    b"\x02" + self._public_key.raw_compressed()[1:] + index_bytes
                ))
                _hmac: bytes = hmac_sha512(self._chain_code, (
                    b"\x03" + self._public_key.raw_compressed()[1:] + index_bytes
                ))

                def new_public_key_point(public_key: IPublicKey, zl: bytes, ecc: EllipticCurveCryptography) -> IPoint:
                    zl: int = bytes_to_integer(zl[:28], endianness="little")
                    return public_key.point() + ((zl * 8) * ecc.generator())

                z_hmacl, z_hmacr, _hmacl, _hmacr = (
                    z_hmac[:hmac_half_length], z_hmac[hmac_half_length:],
                    _hmac[:hmac_half_length], _hmac[hmac_half_length:]
                )

                new_public_key_point: IPoint = new_public_key_point(
                    public_key=self._public_key, zl=z_hmacl, ecc=self._ecc
                )
                # If the public key is the identity point (0, 1) discard the child
                if new_public_key_point.x() == 0 and new_public_key_point.y() == 1:
                    raise ValueError("Computed public child key is not valid, very unlucky index")
                new_public_key: IPublicKey = self._ecc.public_key_class().from_point(
                    new_public_key_point
                )
                self._parent_fingerprint = get_bytes(self.finger_print())
                self._chain_code, self._public_key = (
                    _hmacr, new_public_key
                )
                self._depth, self._index, self._fingerprint = (
                    (self._depth + 1), index, get_bytes(self.finger_print())
                )

            return self

        elif self._ecc.name() in [
            "SLIP10-Ed25519", "SLIP10-Ed25519-Blake2b"
        ]:
            index_bytes: bytes = struct.pack(">L", index)
            data_bytes: bytes = (
                PRIVATE_KEY_PREFIX + self._private_key.raw() + index_bytes
            )

            _hmac: bytes = (
                hmac.digest(
                    self._chain_code, data_bytes, "sha512"
                ) if hasattr(hmac, "digest") else hmac.new(
                    self._chain_code, data_bytes, hashlib.sha512
                ).digest()
            )
            _hmacl, _hmacr = _hmac[:hmac_half_length], _hmac[hmac_half_length:]

            new_private_key: IPrivateKey = self._ecc.private_key_class().from_bytes(_hmacl)

            self._parent_fingerprint = get_bytes(self.finger_print())
            self._private_key, self._chain_code, self._public_key = (
                new_private_key, _hmacr, new_private_key.public_key()
            )
            self._depth, self._index, self._fingerprint = (
                (self._depth + 1), index, get_bytes(self.finger_print())
            )

        elif self._ecc.name() in [
            "SLIP10-Nist256p1", "SLIP10-Secp256k1"
        ]:
            index_bytes: bytes = struct.pack(">L", index)
            if not self._root_private_key and not self._root_public_key:
                raise ValueError("You can't drive this master key")
            if not self._chain_code:
                raise ValueError("You can't drive xprivate_key and private_key")

            if index & 0x80000000:
                if self._private_key is None:
                    raise ValueError("Hardened derivation path is invalid for xpublic key")
                data_bytes: bytes = (
                    PRIVATE_KEY_PREFIX + self._private_key.raw() + index_bytes
                )
            else:
                data_bytes: bytes = (
                    self._public_key.raw_compressed() + index_bytes
                )

            _hmac: bytes = (
                hmac.digest(
                    self._chain_code, data_bytes, "sha512"
                ) if hasattr(hmac, "digest") else hmac.new(
                    self._chain_code, data_bytes, hashlib.sha512
                ).digest()
            )
            _hmacl, _hmacr = _hmac[:hmac_half_length], _hmac[hmac_half_length:]

            _hmacl_int: int = bytes_to_integer(_hmacl)
            if _hmacl_int > self._ecc.order():
                return None

            if self._private_key:
                private_key_int: int = bytes_to_integer(self._private_key.raw())
                key_int = (_hmacl_int + private_key_int) % self._ecc.order()
                if key_int == 0:
                    return None

                new_private_key: IPrivateKey = self._ecc.private_key_class().from_bytes((
                    PRIVATE_KEY_PREFIX * 32 + integer_to_bytes(key_int)
                )[-32:])

                self._parent_fingerprint = get_bytes(self.finger_print())
                self._private_key, self._chain_code, self._public_key = (
                    new_private_key, _hmacr, new_private_key.public_key()
                )
                self._depth, self._index, self._fingerprint = (
                    (self._depth + 1), index, get_bytes(self.finger_print())
                )
            else:
                new_public_key_point: IPoint = (
                    self._public_key.point() + (self._ecc.generator() * bytes_to_integer(_hmacl))
                )
                new_public_key: IPublicKey = self._ecc.public_key_class().from_point(
                    new_public_key_point
                )

                self._parent_fingerprint = get_bytes(self.finger_print())
                self._chain_code, self._public_key = (
                    _hmacr, new_public_key
                )
                self._depth, self._index, self._fingerprint = (
                    (self._depth + 1), index, get_bytes(self.finger_print())
                )
        return self

    def root_private_key(self) -> str:
        return bytes_to_string(self._root_private_key.raw())

    def root_public_key(self, public_key_type: str = "compressed") -> str:
        if public_key_type == "uncompressed":
            return bytes_to_string(self._root_public_key.raw_uncompressed())
        elif public_key_type == "compressed":
            return bytes_to_string(self._root_public_key.raw_compressed())
        raise ValueError("Invalid public key type")

    def xprivate_key(self, encoded: bool = True) -> str:
        return bytes_to_string(self._private_key.raw())

    def xpublic_key(self, encoded: bool = True) -> str:
        return bytes_to_string(self._public_key.raw_compressed())

    def private_key(self) -> str:
        return bytes_to_string(self._private_key.raw())

    def wif(self) -> Optional[str]:
        return private_key_to_wif(
            private_key=self.private_key(), wif_type=self._wif_type
        )

    def chain_code(self) -> str:
        return bytes_to_string(self._chain_code)

    def public_key(self) -> str:
        if self._public_key_type == "uncompressed":
            return self.uncompressed()
        elif self._public_key_type == "compressed":
            return self.compressed()
        else:
            raise ValueError("Invalid Electrum v1 public key mode")

    def compressed(self) -> str:
        return bytes_to_string(self._public_key.raw_compressed())

    def uncompressed(self) -> str:
        return bytes_to_string(self._public_key.raw_uncompressed())

    def hash(self):
        return bytes_to_string(ripemd160(sha256(get_bytes(self.public_key())).digest()))

    def finger_print(self) -> str:
        return self.hash()[:8]

    def parent_finger_print(self) -> str:
        return bytes_to_string(self._parent_fingerprint)

    def depth(self) -> int:
        return self._depth

    def path(self) -> str:
        return self._path

    def index(self) -> int:
        return self._index

    def indexes(self) -> List[int]:
        return self._indexes

    def address(self, network_version: int = 0x00) -> str:
        return P2PKHAddress.encode(
            public_key=self._public_key,
            network_version=network_version,
            public_key_type=self._public_key_type
        )
