#!/usr/bin/env python3

from binascii import unhexlify
from typing import (
    Any, Union
)

import hashlib

from ..libs.base32 import (
    encode_no_padding, decode
)
from ..ecc import (
    IPublicKey, SLIP10Secp256k1PublicKey
)
from ..utils import integer_to_bytes
from . import (
    IAddress, validate_and_get_public_key
)


class FilecoinAddress(IAddress):

    alphabet: str = "abcdefghijklmnopqrstuvwxyz234567"
    address_prefix: str = "f"
    address_types: dict = {
        "secp256k1": 1,  # A SECP256K1 public key address.
        "bls": 3  # A BLS public key address.
    }

    @classmethod
    def compute_checksum(cls, public_key_hash: bytes, address_type: int) -> bytes:
        return hashlib.blake2b(
            (integer_to_bytes(address_type) + public_key_hash), digest_size=4
        ).digest()

    @classmethod
    def encode(cls, public_key: Union[bytes, str, IPublicKey], **kwargs: Any) -> str:

        public_key: SLIP10Secp256k1PublicKey = validate_and_get_public_key(
            public_key=public_key, public_key_cls=SLIP10Secp256k1PublicKey
        )
        public_key_hash: bytes = hashlib.blake2b(
            public_key.raw_uncompressed(), digest_size=20
        ).digest()

        if not kwargs.get("address_type") or \
                kwargs.get("address_type") == "secp256k1":
            address_type: int = cls.address_types["secp256k1"]
        elif kwargs.get("address_type") == "bls":
            address_type: int = cls.address_types["bls"]
        else:
            raise ValueError("Invalid filecoin address type")

        checksum: bytes = cls.compute_checksum(public_key_hash, address_type)
        base32_encode: str = encode_no_padding(
            (public_key_hash + checksum).hex(), cls.alphabet
        )

        return (
            cls.address_prefix + chr(address_type + ord("0")) + base32_encode
        )

    @classmethod
    def decode(cls, address: str, **kwargs: Any) -> str:

        prefix_got: str = address[:len(cls.address_prefix)]
        if cls.address_prefix != prefix_got:
            raise ValueError(f"Invalid prefix (expected {cls.address_prefix!r}, got {prefix_got!r})")
        address_no_prefix: str = address[len(cls.address_prefix):]

        if not kwargs.get("address_type") or \
                kwargs.get("address_type") == "secp256k1":
            address_type: int = cls.address_types["secp256k1"]
        elif kwargs.get("address_type") == "bls":
            address_type: int = cls.address_types["bls"]
        else:
            raise ValueError("Invalid filecoin address type")

        address_type_got = ord(address_no_prefix[0]) - ord("0")
        if address_type != address_type_got:
            raise ValueError(f"Invalid address type (expected {address_type}, got {address_type_got})")

        address_decode: bytes = unhexlify(decode(address_no_prefix[1:], cls.alphabet))

        if len(address_decode) != 24:
            raise ValueError(f"Invalid length (expected {24}, got {len(address_decode)})")

        checksum: bytes = address_decode[-1 * 4:]
        public_key_hash: bytes = address_decode[:-1 * 4]

        checksum_got: bytes = cls.compute_checksum(public_key_hash, address_type)
        if checksum != checksum_got:
            raise ValueError(f"Invalid checksum (expected {checksum.hex()}, got {checksum_got.hex()})")

        return public_key_hash.hex()
