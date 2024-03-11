#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Any, Union, Optional
)

from ..libs.base58 import (
    ensure_string, encode, decode
)
from ..ecc import (
    IPublicKey, SLIP10Secp256k1PublicKey, validate_and_get_public_key
)
from ..cryptocurrencies import Ergo
from ..crypto import blake2b_256
from ..utils import (
    integer_to_bytes, bytes_to_string
)
from .iaddress import IAddress


class ErgoAddress(IAddress):

    checksum_length: int = Ergo.PARAMS.CHECKSUM_LENGTH
    address_type: Optional[int] = None
    network_type: Optional[int] = None
    address_types: dict = {
        "p2pkh": Ergo.PARAMS.ADDRESS_TYPES.P2PKH,
        "p2sh": Ergo.PARAMS.ADDRESS_TYPES.P2SH
    }
    network_types: dict = {
        "mainnet": Ergo.NETWORKS.MAINNET.TYPE,
        "testnet": Ergo.NETWORKS.TESTNET.TYPE
    }

    @staticmethod
    def name() -> str:
        return "Ergo"

    @classmethod
    def compute_checksum(cls, public_key: bytes) -> bytes:
        return blake2b_256(public_key)[:cls.checksum_length]

    @classmethod
    def encode(cls, public_key: Union[bytes, str, IPublicKey], **kwargs: Any) -> str:

        if not kwargs.get("address_type"):
            raise TypeError("Ergo address type is required")
        elif kwargs.get("address_type") == "p2pkh":
            cls.address_type = cls.address_types["p2pkh"]
        elif kwargs.get("address_type") == "p2sh":
            cls.address_type = cls.address_types["p2sh"]
        else:
            raise ValueError("Wrong ergo address type")

        public_key: IPublicKey = validate_and_get_public_key(
            public_key=public_key, public_key_cls=SLIP10Secp256k1PublicKey
        )

        if not kwargs.get("network_type"):
            raise TypeError("Ergo address type is required")
        elif kwargs.get("network_type") == "mainnet":
            cls.network_type = cls.network_types["mainnet"]
        elif kwargs.get("network_type") == "testnet":
            cls.network_type = cls.network_types["testnet"]
        else:
            raise ValueError("Wrong ergo network type")

        prefix: bytes = integer_to_bytes(cls.address_type + cls.network_type)
        address_payload: bytes = prefix + public_key.raw_compressed()
        checksum: bytes = cls.compute_checksum(address_payload)

        return ensure_string(encode(
            address_payload + checksum
        ))

    @classmethod
    def decode(cls, address: str, **kwargs: Any) -> str:

        if not kwargs.get("address_type"):
            raise TypeError("Ergo address type is required")
        elif kwargs.get("address_type") == "p2pkh":
            cls.address_type = cls.address_types["p2pkh"]
        elif kwargs.get("address_type") == "p2sh":
            cls.address_type = cls.address_types["p2sh"]
        else:
            raise ValueError("Wrong ergo address type")

        if not kwargs.get("network_type"):
            raise TypeError("Ergo address type is required")
        elif kwargs.get("network_type") == "mainnet":
            cls.network_type = cls.network_types["mainnet"]
        elif kwargs.get("network_type") == "testnet":
            cls.network_type = cls.network_types["testnet"]
        else:
            raise ValueError("Wrong ergo network type")

        prefix: bytes = integer_to_bytes(cls.address_type + cls.network_type)
        address_decode: bytes = decode(address)

        expected_length: int = SLIP10Secp256k1PublicKey.compressed_length() + cls.checksum_length + 1
        if len(address_decode) != expected_length:
            raise ValueError(f"Invalid length (expected: {expected_length}, got: {len(address_decode)})")

        checksum: bytes = address_decode[-1 * cls.checksum_length:]
        address_with_prefix: bytes = address_decode[:-1 * cls.checksum_length]

        checksum_got: bytes = cls.compute_checksum(address_with_prefix)
        if checksum != checksum_got:
            raise ValueError(f"Invalid checksum (expected: {checksum.hex()}, got: {checksum_got.hex()})")

        prefix_got: bytes = address_with_prefix[:len(prefix)]
        if prefix != prefix_got:
            raise ValueError(f"Invalid prefix (expected: {prefix}, got: {prefix_got})")
        public_key: bytes = address_with_prefix[len(prefix):]

        if not SLIP10Secp256k1PublicKey.is_valid_bytes(public_key):
            raise ValueError(f"Invalid {SLIP10Secp256k1PublicKey.name()} public key {public_key.hex()}")

        return bytes_to_string(public_key)
