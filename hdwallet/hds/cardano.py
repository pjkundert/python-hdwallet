#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Optional

import hashlib
import cbor2

from ..ecc import (
    EllipticCurveCryptography, IPoint, IPublicKey, KholawEd25519PrivateKey
)
from ..crypto import (
    pbkdf2_hmac_sha512, hmac_sha512, hmac_sha256, sha512
)
from ..cryptocurrencies import Cardano
from ..utils import (
    get_bytes, reset_bits, set_bits, add_no_carry, multiply_scalar_no_carry, bytes_to_string, are_bits_set, integer_to_bytes, bytes_to_integer
)
from ..addresses.cardano import CardanoAddress
from .bip32 import BIP32HD


class CardanoHD(BIP32HD):

    cardano_type: str

    def __init__(self, cardano_type: str) -> None:
        super(CardanoHD, self).__init__(
            ecc_name="Kholaw-Ed25519"
        )
        if cardano_type not in Cardano.TYPES.__dict__.values():
            raise ValueError("Invalid Cardano type")
        self.cardano_type = cardano_type

    @classmethod
    def name(cls) -> str:
        return "Cardano"

    def from_seed(self, seed: str, passphrase: Optional[str] = None) -> "CardanoHD":

        self._seed = get_bytes(seed)

        if self.cardano_type == "byron-legacy":
            if len(self._seed) != 32:
                raise ValueError(f"Invalid seed length ({len(self._seed)})")

            def tweak_master_key_bits(data: bytes) -> bytes:
                data: bytearray = bytearray(data)
                # Clear the lowest 3 bits of the first byte of kL
                data[0] = reset_bits(data[0], 0x07)
                # Clear the highest bit of the last byte of kL
                data[31] = reset_bits(data[31], 0x80)
                # Set the second-highest bit of the last byte of kL
                data[31] = set_bits(data[31], 0x40)
                return bytes(data)

            data: bytes = cbor2.dumps(self._seed)
            iteration_number: int = 1

            success: bool = True
            while success:

                i: bytes = hmac_sha512(
                    data, b"Root Seed Chain %d" % iteration_number
                )
                il: bytes = i[:hashlib.sha512().digest_size // 2]
                ir: bytes = i[hashlib.sha512().digest_size // 2:]
                il: bytes = tweak_master_key_bits(sha512(il))

                success = are_bits_set(il[31], 0x20)
                if success:
                    iteration_number += 1

                self._root_private_key = self._ecc.private_key_class().from_bytes(il)
                self._root_chain_code = ir

        elif self.cardano_type in [
            "byron-icarus", "shelley-icarus"
        ]:
            if len(self._seed) < 16:
                raise ValueError(f"Invalid seed length ({len(self._seed)})")

            pbkdf2_passphrase, pbkdf2_rounds, pbkdf2_output_length = (
                (passphrase if passphrase else ""), 4096, 96
            )

            def tweak_master_key_bits(data: bytes) -> bytes:

                data: bytearray = bytearray(data)
                # Clear the lowest 3 bits of the first byte of kL
                data[0] = reset_bits(data[0], 0x07)
                # Clear the highest 3 bits of the last byte of kL (standard kholaw only clears the highest one)
                data[31] = reset_bits(data[31], 0xE0)
                # Set the second-highest bit of the last byte of kL
                data[31] = set_bits(data[31], 0x40)

                return bytes(data)

            key: bytes = tweak_master_key_bits(pbkdf2_hmac_sha512(
                pbkdf2_passphrase, self._seed, pbkdf2_rounds, pbkdf2_output_length
            ))

            self._root_private_key, self._root_chain_code = (
                self._ecc.private_key_class().from_bytes(
                    key[:KholawEd25519PrivateKey.length()]
                ), key[KholawEd25519PrivateKey.length():]
            )

        elif self.cardano_type in [
            "byron-ledger", "shelley-ledger"
        ]:
            if len(self._seed) < 16:
                raise ValueError(f"Invalid seed length ({len(self._seed)})")

            hmac_half_length: int = hashlib.sha512().digest_size // 2

            # Compute HMAC, retry if the resulting private key is not valid
            self._hmac: bytes = b""
            hmac_data: bytes = self._seed
            success: bool = False

            while not success:
                self._hmac = hmac_sha512(
                    self.get_hmac(ecc_name=self._ecc_name), hmac_data
                )
                # Compute kL and kR
                success = ((self._hmac[:hmac_half_length][31] & 0x20) == 0)
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

            # Compute kL and kR
            kl: bytes = self._hmac[:hmac_half_length]
            kr: bytes = self._hmac[hmac_half_length:]
            # Tweak kL bytes
            kl: bytes = tweak_master_key_bits(kl)
            chain_code: bytes = hmac_sha256(
                self.get_hmac(ecc_name=self._ecc_name), b"\x01" + self._seed
            )
            self._root_private_key, self._root_chain_code = (
                self._ecc.private_key_class().from_bytes(
                    (kl + kr)
                ), chain_code
            )

        self._root_public_key = self._root_private_key.public_key()
        self._private_key, self._chain_code, self._parent_fingerprint = (
            self._root_private_key, self._root_chain_code, b"\x00\x00\x00\x00"
        )
        self._public_key = self._private_key.public_key()

        return self

    def drive(self, index: int) -> Optional["CardanoHD"]:

        hmac_half_length: int = hashlib.sha512().digest_size // 2

        if self.cardano_type == "byron-legacy":
            index_bytes: bytes = integer_to_bytes(
                data=index, bytes_num=4, endianness="big"
            )
        else:
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
                if self.cardano_type == "byron-legacy":
                    zl: int = bytes_to_integer(
                        multiply_scalar_no_carry(zl, 8), endianness="little"
                    )
                    kl: int = bytes_to_integer(kl, endianness="little")

                    return integer_to_bytes(
                        (zl + kl) % ecc.order(), bytes_num=32, endianness="little"
                    )
                else:
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
                if self.cardano_type == "byron-legacy":
                    return add_no_carry(zr, kr)
                else:
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
                get_bytes(self.fingerprint())
            )
            self._public_key = self._private_key.public_key()
            self._depth, self._index, self._fingerprint = (
                (self._depth + 1), index, get_bytes(self.fingerprint())
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
                if self.cardano_type == "byron-legacy":
                    zl: int = bytes_to_integer(multiply_scalar_no_carry(zl, 8), endianness="little")
                    return public_key.point() + (zl * ecc.generator())
                else:
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
            self._parent_fingerprint = get_bytes(self.fingerprint())
            self._chain_code, self._public_key = (
                _hmacr, new_public_key
            )
            self._depth, self._index, self._fingerprint = (
                (self._depth + 1), index, get_bytes(self.fingerprint())
            )
        return self

    def path_key(self) -> Optional[str]:
        if self.cardano_type == "byron-legacy":
            self._root_public_key = self._root_private_key.public_key()
            return bytes_to_string(pbkdf2_hmac_sha512(
                (self._root_public_key.raw_compressed()[1:] + self._root_chain_code), "address-hashing", 500, 32
            ))
        return None

    def address(self, **kwargs) -> str:
        if self.cardano_type == "byron-legacy":
            return CardanoAddress.encode_byron_legacy(
                public_key=self._public_key,
                path=self.path(),
                path_key=self.path_key(),
                chain_code=self._chain_code,
                address_type=kwargs.get(
                    "address_type", "public-key"
                )
            )
        elif self.cardano_type in ["byron-icarus", "byron-ledger"]:
            return CardanoAddress.encode_byron_icarus(
                public_key=self._public_key,
                chain_code=self._chain_code,
                address_type=kwargs.get(
                    "address_type", "public-key"
                )
            )
        elif self.cardano_type in ["shelley-icarus", "shelley-ledger"]:
            if kwargs.get("address_type") in ["payment", "shelley-payment"]:
                if not kwargs.get("staking_public_key"):
                    raise ValueError("staking_public_key param is required for payment address type")
                return CardanoAddress.encode_shelley(
                    public_key=self._public_key,
                    staking_public_key=kwargs.get("staking_public_key"),
                    network=kwargs.get("network", "mainnet")
                )
            elif kwargs.get("address_type") in ["staking", "shelley-staking", "reward", "shelley-reward"]:
                return CardanoAddress.encode_shelley_staking(
                    public_key=self._public_key,
                    network=kwargs.get("network", "mainnet")
                )
            raise ValueError(
                f"address_type param is required for Cardano {self.cardano_type} type, with 'payment', 'staking', or 'reward' values"
            )
