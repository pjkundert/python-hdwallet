#!/usr/bin/env python3

from binascii import unhexlify
from typing import (
    Any, Union
)
from Crypto.Hash import SHA3_256

import hashlib

from ..ecc import (
    IPublicKey, SLIP10Secp256k1PublicKey
)
from . import (
    IAddress, validate_and_get_public_key
)


class IconAddress(IAddress):

    address_prefix: str = "hx"
    key_hash_length: int = 20

    @classmethod
    def encode(cls, public_key: Union[bytes, str, IPublicKey], **kwargs: Any) -> str:

        public_key: SLIP10Secp256k1PublicKey = validate_and_get_public_key(
            public_key=public_key, public_key_cls=SLIP10Secp256k1PublicKey
        )
        public_key_hash: bytes = (
            hashlib.new("sha3_256", public_key.raw_uncompressed()[1:]).digest()
            if "sha3_256" in hashlib.algorithms_available else
            SHA3_256.new(public_key.raw_uncompressed()[1:]).digest()
        )[-cls.key_hash_length:]

        return cls.address_prefix + public_key_hash.hex()

    @classmethod
    def decode(cls, address: str, **kwargs: Any) -> str:

        prefix_got: str = address[:len(cls.address_prefix)]
        if cls.address_prefix != prefix_got:
            raise ValueError(f"Invalid prefix (expected {cls.address_prefix!r}, got {prefix_got!r})")
        address_no_prefix: str = address[len(cls.address_prefix):]

        public_key_hash: bytes = unhexlify(address_no_prefix)

        if len(public_key_hash) != cls.key_hash_length:
            raise ValueError(f"Invalid length (expected {cls.key_hash_length}, got {len(public_key_hash)})")

        return public_key_hash.hex()
