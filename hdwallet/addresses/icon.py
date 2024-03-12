#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Any, Union
)

from ..ecc import (
    IPublicKey, SLIP10Secp256k1PublicKey, validate_and_get_public_key
)
from ..cryptocurrencies import ICON
from ..crypto import sha3_256
from ..utils import (
    get_bytes, bytes_to_string
)
from .iaddress import IAddress


class IconAddress(IAddress):

    address_prefix: str = ICON.PARAMS.ADDRESS_PREFIX
    key_hash_length: int = ICON.PARAMS.KEY_HASH_LENGTH

    @staticmethod
    def name() -> str:
        return "Icon"

    @classmethod
    def encode(cls, public_key: Union[bytes, str, IPublicKey], **kwargs: Any) -> str:

        public_key: IPublicKey = validate_and_get_public_key(
            public_key=public_key, public_key_cls=SLIP10Secp256k1PublicKey
        )
        public_key_hash: bytes = sha3_256(
            public_key.raw_uncompressed()[1:]
        )[-cls.key_hash_length:]

        return cls.address_prefix + bytes_to_string(public_key_hash)

    @classmethod
    def decode(cls, address: str, **kwargs: Any) -> str:

        prefix_got: str = address[:len(cls.address_prefix)]
        if cls.address_prefix != prefix_got:
            raise ValueError(f"Invalid prefix (expected: {cls.address_prefix}, got: {prefix_got})")
        address_no_prefix: str = address[len(cls.address_prefix):]

        public_key_hash: bytes = get_bytes(address_no_prefix)

        if len(public_key_hash) != cls.key_hash_length:
            raise ValueError(f"Invalid length (expected: {cls.key_hash_length}, got: {len(public_key_hash)})")

        return bytes_to_string(public_key_hash)
