#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Optional, Union, List, Type
)
from hashlib import sha256

import hmac
import hashlib
import struct

from ..libs.ripemd160 import ripemd160
from ..libs.base58 import check_decode
from ..ecc import (
    IPoint, IPublicKey, IPrivateKey, IEllipticCurveCryptography, KholawEd25519PrivateKey, SLIP10Ed25519PublicKey, SLIP10Ed25519PrivateKey
)
from ..seeds import ISeed
from ..derivations import IDerivation
from ..addresses import (
    P2PKHAddress, P2SHAddress, P2TRAddress, P2WPKHAddress, P2WPKHInP2SHAddress, P2WSHAddress, P2WSHInP2SHAddress
)
from ..const import (
    PUBLIC_KEY_TYPES, WIF_TYPES
)
from ..cryptocurrencies import Bitcoin
from ..crypto import hmac_sha512
from ..wif import (
    private_key_to_wif, wif_to_private_key
)
from ..keys import (
    serialize, deserialize
)
from ..exceptions import (
    Error, AddressError, DerivationError, ExtendedKeyError
)
from ..utils import (
    get_bytes, get_hmac, bytes_to_integer, integer_to_bytes, bytes_to_string, reset_bits, set_bits
)
from .ihd import IHD


class BIP32HD(IHD):

    _ecc: IEllipticCurveCryptography
    _seed: Optional[bytes] = None
    _hmac: Optional[bytes] = None
    _root_private_key: Optional[IPrivateKey] = None
    _root_chain_code: Optional[bytes] = None
    _root_public_key: Optional[IPublicKey] = None
    _private_key: Optional[IPrivateKey] = None
    _chain_code: Optional[bytes] = None
    _public_key: Optional[IPublicKey] = None
    _public_key_type: str = PUBLIC_KEY_TYPES.COMPRESSED
    _wif_type: str = WIF_TYPES.WIF_COMPRESSED
    _fingerprint: Optional[bytes] = None
    _parent_fingerprint: Optional[bytes] = None
    _indexes: List[int] = []
    _path: str = "m/"
    _root_depth: int = 0
    _root_index: int = 0
    _depth: int = 0
    _index: int = 0
    
    def __init__(
        self, ecc: Type[IEllipticCurveCryptography], public_key_type: str = PUBLIC_KEY_TYPES.COMPRESSED, **kwargs
    ) -> None:
        super(BIP32HD, self).__init__(**kwargs)

        self._ecc: IEllipticCurveCryptography = ecc.__call__()
        if public_key_type == PUBLIC_KEY_TYPES.UNCOMPRESSED:
            self._wif_type = WIF_TYPES.WIF
        elif public_key_type == PUBLIC_KEY_TYPES.COMPRESSED:
            self._wif_type = WIF_TYPES.WIF_COMPRESSED
        else:
            raise Error(
                f"Invalid {self.name()} public key type",
                expected=PUBLIC_KEY_TYPES.get_types(),
                got=public_key_type
            )
        self._public_key_type = public_key_type

    @classmethod
    def name(cls) -> str:
        return "BIP32"

    def __update__(self) -> "BIP32HD":
        return self

    def from_seed(self, seed: Union[bytes, str, ISeed], **kwargs) -> "BIP32HD":

        self._seed = get_bytes(
            seed.seed() if isinstance(seed, ISeed) else seed
        )
        if len(self._seed) < 16:
            raise Error(f"Invalid seed length", expected="< 16", got=len(self._seed))

        hmac_half_length: int = hashlib.sha512().digest_size // 2

        self._hmac: bytes = b""
        hmac_data: bytes = self._seed
        success: bool = False

        while not success:
            self._hmac = hmac.digest(
                get_hmac(ecc_name=self._ecc.NAME), hmac_data, "sha512"
            ) if hasattr(hmac, "digest") else hmac.new(
                get_hmac(ecc_name=self._ecc.NAME), hmac_data, hashlib.sha512
            ).digest()

            if self._ecc.NAME == "Kholaw-Ed25519":
                success = ((self._hmac[:hmac_half_length][31] & 0x20) == 0)
                if not success:
                    hmac_data = self._hmac
            else:
                private_key_class: IPrivateKey = self._ecc.PRIVATE_KEY
                success = private_key_class.is_valid_bytes(self._hmac[:hmac_half_length])
                if not success:
                    hmac_data = self._hmac

        def tweak_master_key_bits(data: bytes) -> bytes:

            data: bytearray = bytearray(data)
            data[0] = reset_bits(data[0], 0x07)
            data[31] = reset_bits(data[31], 0x80)
            data[31] = set_bits(data[31], 0x40)

            return bytes(data)

        if self._ecc.NAME == "Kholaw-Ed25519":
            kl_bytes, kr_bytes = (
                self._hmac[:hmac_half_length], self._hmac[hmac_half_length:]
            )
            kl_bytes = tweak_master_key_bits(kl_bytes)

            chain_code_bytes = hmac.digest(
                get_hmac(ecc_name=self._ecc.NAME), b"\x01" + self._seed, "sha256"
            ) if hasattr(hmac, "digest") else hmac.new(
                get_hmac(ecc_name=self._ecc.NAME), b"\x01" + self._seed, hashlib.sha256
            ).digest()

            self._root_private_key, self._root_chain_code = (
                self._ecc.PRIVATE_KEY.from_bytes(
                    (kl_bytes + kr_bytes)
                ), chain_code_bytes
            )
        else:
            self._root_private_key, self._root_chain_code = (
                self._ecc.PRIVATE_KEY.from_bytes(
                    self._hmac[:hmac_half_length]
                ), self._hmac[hmac_half_length:]
            )

        self._private_key, self._chain_code, self._parent_fingerprint = (
            self._root_private_key, self._root_chain_code, (integer_to_bytes(0x00) * 4)
        )
        self._root_public_key = self._root_private_key.public_key()
        self._public_key = self._root_public_key
        self.__update__()
        return self

    def from_xprivate_key(self, xprivate_key: str, encoded: bool = True) -> "BIP32HD":

        if len(check_decode(xprivate_key) if encoded else xprivate_key) != 78:
            raise ExtendedKeyError("Invalid extended(x) private key")

        version, depth, parent_fingerprint, index, chain_code, key = deserialize(
            key=xprivate_key, encoded=encoded
        )

        self._root_chain_code = chain_code
        self._root_private_key = self._ecc.PRIVATE_KEY.from_bytes(key[1:])
        self._root_public_key = self._root_private_key.public_key()
        self._root_depth = depth
        self._parent_fingerprint = parent_fingerprint
        self._root_index = index
        self._chain_code = self._root_chain_code
        self._private_key = self._root_private_key
        self._public_key = self._root_public_key
        self._depth = self._root_depth
        self._index = self._root_index
        self.__update__()
        return self

    def from_xpublic_key(self, xpublic_key: str, encoded: bool = True) -> "BIP32HD":

        if len(check_decode(xpublic_key) if encoded else xpublic_key) != 78:
            raise ExtendedKeyError("Invalid extended(x) public key")

        version, depth, parent_fingerprint, index, chain_code, key = deserialize(
            key=xpublic_key, encoded=encoded
        )

        self._root_chain_code = chain_code
        self._root_public_key = self._ecc.PUBLIC_KEY.from_bytes(key)
        self._root_depth = depth
        self._parent_fingerprint = parent_fingerprint
        self._root_index = index
        self._chain_code = self._root_chain_code
        self._public_key = self._root_public_key
        self._depth = self._root_depth
        self._index = self._root_index
        self.__update__()
        return self

    def from_wif(self, wif: str) -> "BIP32HD":
        self.from_private_key(private_key=wif_to_private_key(wif=wif))
        self.__update__()
        return self

    def from_private_key(self, private_key: str) -> "BIP32HD":
        self._private_key = SLIP10Ed25519PrivateKey.from_bytes(get_bytes(private_key))
        self._public_key = self._private_key.public_key()
        self.__update__()
        return self

    def from_public_key(self, public_key: str) -> "BIP32HD":
        self._public_key = SLIP10Ed25519PublicKey.from_bytes(get_bytes(public_key))
        self.__update__()
        return self

    def from_derivation(self, derivation: IDerivation) -> "BIP32HD":

        if not isinstance(derivation, IDerivation):
            raise DerivationError("Invalid derivation instance", expected=IDerivation, got=type(derivation))

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

    def update_derivation(self, derivation: IDerivation) -> "BIP32HD":

        self.clean_derivation()
        self.from_derivation(
            derivation=derivation
        )
        return self

    def clean_derivation(self) -> "BIP32HD":
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

    def drive(self, index: int) -> Optional["BIP32HD"]:

        hmac_half_length: int = hashlib.sha512().digest_size // 2

        if self._ecc.NAME == "Kholaw-Ed25519":
            index_bytes: bytes = integer_to_bytes(
                data=index, bytes_num=4, endianness="little"
            )
            if self._private_key:
                if index & 0x80000000:
                    if self._private_key is None:
                        raise DerivationError("Hardened derivation path is invalid for xpublic key")
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

                def new_private_key_left_part(zl: bytes, kl: bytes, ecc: IEllipticCurveCryptography) -> bytes:
                    zl: int = bytes_to_integer(zl[:28], endianness="little")
                    kl: int = bytes_to_integer(kl, endianness="little")

                    private_key_left: int = (zl * 8) + kl
                    if private_key_left % ecc.ORDER == 0:
                        raise Error("Computed child key is not valid, very unlucky index")

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
                    self._ecc.PRIVATE_KEY.from_bytes(
                        kl_bytes + kr_bytes
                    ),
                    _hmacr,
                    get_bytes(self.fingerprint())
                )
                self._public_key = self._private_key.public_key()
                self._depth, self._index, self._fingerprint = (
                    (self._depth + 1), index, get_bytes(self.fingerprint())
                )
            else:
                if index & 0x80000000:
                    raise DerivationError("Hardened derivation path is invalid for xpublic key")
                z_hmac: bytes = hmac_sha512(self._chain_code, (
                    b"\x02" + self._public_key.raw_compressed()[1:] + index_bytes
                ))
                _hmac: bytes = hmac_sha512(self._chain_code, (
                    b"\x03" + self._public_key.raw_compressed()[1:] + index_bytes
                ))

                def new_public_key_point(public_key: IPublicKey, zl: bytes, ecc: IEllipticCurveCryptography) -> IPoint:
                    zl: int = bytes_to_integer(zl[:28], endianness="little")
                    return public_key.point() + ((zl * 8) * ecc.GENERATOR)

                z_hmacl, z_hmacr, _hmacl, _hmacr = (
                    z_hmac[:hmac_half_length], z_hmac[hmac_half_length:],
                    _hmac[:hmac_half_length], _hmac[hmac_half_length:]
                )

                new_public_key_point: IPoint = new_public_key_point(
                    public_key=self._public_key, zl=z_hmacl, ecc=self._ecc
                )
                if new_public_key_point.x() == 0 and new_public_key_point.y() == 1:
                    raise Error("Computed public child key is not valid, very unlucky index")
                new_public_key: IPublicKey = self._ecc.PUBLIC_KEY.from_point(
                    new_public_key_point
                )
                self._parent_fingerprint = get_bytes(self.fingerprint())
                self._chain_code, self._public_key = (
                    _hmacr, new_public_key
                )
                self._depth, self._index, self._fingerprint = (
                    (self._depth + 1), index, get_bytes(self.fingerprint())
                )

            return self

        elif self._ecc.NAME in [
            "SLIP10-Ed25519", "SLIP10-Ed25519-Blake2b", "SLIP10-Ed25519-Monero"
        ]:
            index_bytes: bytes = struct.pack(">L", index)
            data_bytes: bytes = (
                integer_to_bytes(0x00) + self._private_key.raw() + index_bytes
            )

            _hmac: bytes = (
                hmac.digest(
                    self._chain_code, data_bytes, "sha512"
                ) if hasattr(hmac, "digest") else hmac.new(
                    self._chain_code, data_bytes, hashlib.sha512
                ).digest()
            )
            _hmacl, _hmacr = _hmac[:hmac_half_length], _hmac[hmac_half_length:]

            new_private_key: IPrivateKey = self._ecc.PRIVATE_KEY.from_bytes(_hmacl)

            self._parent_fingerprint = get_bytes(self.fingerprint())
            self._private_key, self._chain_code, self._public_key = (
                new_private_key, _hmacr, new_private_key.public_key()
            )
            self._depth, self._index, self._fingerprint = (
                (self._depth + 1), index, get_bytes(self.fingerprint())
            )

        elif self._ecc.NAME in [
            "SLIP10-Nist256p1", "SLIP10-Secp256k1"
        ]:
            index_bytes: bytes = struct.pack(">L", index)
            if not self._root_private_key and not self._root_public_key:
                raise DerivationError("You can't drive this master key")
            if not self._chain_code:
                raise DerivationError("You can't drive xprivate_key and private_key")

            if index & 0x80000000:
                if self._private_key is None:
                    raise DerivationError("Hardened derivation path is invalid for xpublic key")
                data_bytes: bytes = (
                    integer_to_bytes(0x00) + self._private_key.raw() + index_bytes
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
            if _hmacl_int > self._ecc.ORDER:
                return None

            if self._private_key:
                private_key_int: int = bytes_to_integer(self._private_key.raw())
                key_int = (_hmacl_int + private_key_int) % self._ecc.ORDER
                if key_int == 0:
                    return None

                new_private_key: IPrivateKey = self._ecc.PRIVATE_KEY.from_bytes((
                    integer_to_bytes(0x00) * 32 + integer_to_bytes(key_int)
                )[-32:])

                self._parent_fingerprint = get_bytes(self.fingerprint())
                self._private_key, self._chain_code, self._public_key = (
                    new_private_key, _hmacr, new_private_key.public_key()
                )
                self._depth, self._index, self._fingerprint = (
                    (self._depth + 1), index, get_bytes(self.fingerprint())
                )
            else:
                new_public_key_point: IPoint = (
                    self._public_key.point() + (self._ecc.GENERATOR * bytes_to_integer(_hmacl))
                )
                new_public_key: IPublicKey = self._ecc.PUBLIC_KEY.from_point(
                    new_public_key_point
                )

                self._parent_fingerprint = get_bytes(self.fingerprint())
                self._chain_code, self._public_key = (
                    _hmacr, new_public_key
                )
                self._depth, self._index, self._fingerprint = (
                    (self._depth + 1), index, get_bytes(self.fingerprint())
                )
        return self

    def seed(self) -> Optional[str]:
        return bytes_to_string(self._seed)

    def root_xprivate_key(
        self, version: Union[bytes, int] = Bitcoin.NETWORKS.MAINNET.XPRIVATE_KEY_VERSIONS.P2PKH, encoded: bool = True
    ) -> Optional[str]:

        return serialize(
            version=(
                integer_to_bytes(version) if isinstance(version, int) else get_bytes(version)
            ),
            depth=self._root_depth,
            parent_fingerprint=(integer_to_bytes(0x00) * 4),
            index=self._root_index,
            chain_code=self.root_chain_code(),
            key=(
                "00" + self.root_private_key()
            ),
            encoded=encoded
        ) if self.root_private_key() else None

    def root_xpublic_key(
        self, version: Union[bytes, int] = Bitcoin.NETWORKS.MAINNET.XPUBLIC_KEY_VERSIONS.P2PKH, encoded: bool = True
    ) -> Optional[str]:

        return serialize(
            version=(
                integer_to_bytes(version) if isinstance(version, int) else get_bytes(version)
            ),
            depth=self._root_depth,
            parent_fingerprint=(integer_to_bytes(0x00) * 4),
            index=self._root_index,
            chain_code=self.root_chain_code(),
            key=self.root_public_key(
                public_key_type="compressed"
            ),
            encoded=encoded
        ) if self.root_public_key(public_key_type="compressed") else None

    def root_private_key(self) -> Optional[str]:
        return bytes_to_string(self._root_private_key.raw()) if self._root_private_key else None

    def root_chain_code(self) -> Optional[str]:
        return bytes_to_string(self._root_chain_code)

    def root_public_key(self, public_key_type: Optional[str] = None) -> Optional[str]:
        if not self._root_public_key:
            return None

        if public_key_type:
            if public_key_type not in PUBLIC_KEY_TYPES.get_types():
                raise Error(
                    f"Invalid {self.name()} public key type",
                    expected=PUBLIC_KEY_TYPES.get_types(),
                    got=public_key_type
                )
            _public_key_type: str = public_key_type
        else:
            _public_key_type: str = self._public_key_type

        if _public_key_type == PUBLIC_KEY_TYPES.UNCOMPRESSED:
            return bytes_to_string(self._root_public_key.raw_uncompressed())
        elif _public_key_type == PUBLIC_KEY_TYPES.COMPRESSED:
            return bytes_to_string(self._root_public_key.raw_compressed())

    def xprivate_key(
        self, version: Union[bytes, int] = Bitcoin.NETWORKS.MAINNET.XPRIVATE_KEY_VERSIONS.P2PKH, encoded: bool = True
    ) -> Optional[str]:

        return serialize(
            version=(
                integer_to_bytes(version) if isinstance(version, int) else get_bytes(version)
            ),
            depth=self._depth,
            parent_fingerprint=self.parent_fingerprint(),
            index=self._index,
            chain_code=self.chain_code(),
            key=("00" + self.private_key()),
            encoded=encoded
        ) if self.private_key() else None

    def xpublic_key(
        self, version: Union[bytes, int] = Bitcoin.NETWORKS.MAINNET.XPUBLIC_KEY_VERSIONS.P2PKH, encoded: bool = True
    ) -> Optional[str]:

        return serialize(
            version=(
                integer_to_bytes(version) if isinstance(version, int) else get_bytes(version)
            ),
            depth=self._depth,
            parent_fingerprint=self.parent_fingerprint(),
            index=self._index,
            chain_code=self.chain_code(),
            key=self.public_key(
                public_key_type="compressed"
            ),
            encoded=encoded
        ) if self.public_key(public_key_type="compressed") else None

    def private_key(self) -> Optional[str]:
        return bytes_to_string(self._private_key.raw()) if self._private_key else None

    def wif(self, wif_type: Optional[str] = None) -> Optional[str]:
        if wif_type:
            if wif_type not in WIF_TYPES.get_types():
                raise Error(
                    f"Invalid {self.name()} WIF type",
                    expected=WIF_TYPES.get_types(),
                    got=wif_type
                )
            _wif_type: str = wif_type
        else:
            _wif_type: str = self._wif_type

        return private_key_to_wif(
            private_key=self.private_key(), wif_type=_wif_type
        ) if self.private_key() else None

    def wif_type(self) -> str:
        return self._wif_type

    def chain_code(self) -> Optional[str]:
        return bytes_to_string(self._chain_code)

    def public_key(self, public_key_type: Optional[str] = None):
        if public_key_type:
            if public_key_type not in PUBLIC_KEY_TYPES.get_types():
                raise Error(
                    f"Invalid {self.name()} public key type",
                    expected=PUBLIC_KEY_TYPES.get_types(),
                    got=public_key_type
                )
            _public_key_type: str = public_key_type
        else:
            _public_key_type: str = self._public_key_type

        if _public_key_type == PUBLIC_KEY_TYPES.UNCOMPRESSED:
            return self.uncompressed()
        elif _public_key_type == PUBLIC_KEY_TYPES.COMPRESSED:
            return self.compressed()

    def public_key_type(self) -> str:
        return self._public_key_type

    def compressed(self) -> str:
        return bytes_to_string(self._public_key.raw_compressed())

    def uncompressed(self) -> str:
        return bytes_to_string(self._public_key.raw_uncompressed())

    def hash(self) -> str:
        return bytes_to_string(ripemd160(sha256(get_bytes(self.public_key())).digest()))

    def fingerprint(self) -> str:
        return self.hash()[:8]

    def parent_fingerprint(self) -> str:
        return bytes_to_string(self._parent_fingerprint)

    def depth(self) -> int:
        return self._depth

    def path(self) -> str:
        return self._path

    def index(self) -> int:
        return self._index

    def indexes(self) -> List[int]:
        return self._indexes

    def address(
        self,
        address: str = Bitcoin.ADDRESSES.P2PKH,
        public_key_address_prefix: int = Bitcoin.NETWORKS.MAINNET.PUBLIC_KEY_ADDRESS_PREFIX,
        script_address_prefix: int = Bitcoin.NETWORKS.MAINNET.SCRIPT_ADDRESS_PREFIX,
        hrp: str = Bitcoin.NETWORKS.MAINNET.HRP,
        witness_version: int = Bitcoin.NETWORKS.MAINNET.WITNESS_VERSIONS.P2WPKH,
        **kwargs
    ) -> str:
        if address == P2PKHAddress.name():
            return P2PKHAddress.encode(
                public_key=self._public_key,
                public_key_address_prefix=public_key_address_prefix,
                public_key_type=self._public_key_type
            )
        elif address == P2SHAddress.name():
            return P2SHAddress.encode(
                public_key=self._public_key,
                script_address_prefix=script_address_prefix,
                public_key_type=self._public_key_type
            )
        elif address == P2TRAddress.name():
            return P2TRAddress.encode(
                public_key=self._public_key,
                hrp=hrp,
                witness_version=witness_version,
                public_key_type=self._public_key_type
            )
        elif address == P2WPKHAddress.name():
            return P2WPKHAddress.encode(
                public_key=self._public_key,
                hrp=hrp,
                witness_version=witness_version,
                public_key_type=self._public_key_type
            )
        elif address == P2WPKHInP2SHAddress.name():
            return P2WPKHInP2SHAddress.encode(
                public_key=self._public_key,
                script_address_prefix=script_address_prefix,
                public_key_type=self._public_key_type
            )
        elif address == P2WSHAddress.name():
            return P2WSHAddress.encode(
                public_key=self._public_key,
                hrp=hrp,
                witness_version=witness_version,
                public_key_type=self._public_key_type
            )
        elif address == P2WSHInP2SHAddress.name():
            return P2WSHInP2SHAddress.encode(
                public_key=self._public_key,
                script_address_prefix=script_address_prefix,
                public_key_type=self._public_key_type
            )
        raise AddressError(
            f"Invalid {self.name()} address",
            expected=[
                P2PKHAddress.name(),
                P2SHAddress.name(),
                P2TRAddress.name(),
                P2WPKHAddress.name(),
                P2WPKHInP2SHAddress.name(),
                P2WSHAddress.name(),
                P2WSHInP2SHAddress.name()
            ],
            got=address
        )
