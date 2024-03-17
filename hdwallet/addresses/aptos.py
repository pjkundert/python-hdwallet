#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Any, Union
)

from ..ecc import (
    IPublicKey, SLIP10Ed25519PublicKey, validate_and_get_public_key
)
from ..cryptocurrencies import Aptos
from ..crypto import sha3_256
from ..utils import (
    bytes_to_string, integer_to_bytes
)
from .iaddress import IAddress


class AptosAddress(IAddress):

    suffix: bytes = integer_to_bytes(Aptos.PARAMS.SUFFIX)
    address_prefix: str = Aptos.PARAMS.ADDRESS_PREFIX

    @staticmethod
    def name() -> str:
        return "Aptos"

    @classmethod
    def encode(cls, public_key: Union[bytes, str, IPublicKey], **kwargs: Any) -> str:

        public_key: IPublicKey = validate_and_get_public_key(
            public_key=public_key, public_key_cls=SLIP10Ed25519PublicKey
        )
        payload: bytes = public_key.raw_compressed()[1:] + cls.suffix
        payload_hash: bytes = sha3_256(payload)
        return cls.address_prefix + bytes_to_string(payload_hash).lstrip("0")

    @classmethod
    def decode(cls, address: str, **kwargs: Any) -> str:

        address_prefix_got: str = address[:len(cls.address_prefix)]
        if cls.address_prefix != address_prefix_got:
            raise ValueError(f"Invalid address_prefix (expected: {cls.address_prefix}, got: {address_prefix_got})")
        address_no_prefix = (address[len(cls.address_prefix):]).rjust(64, "0")

        if len(address_no_prefix) != 64:
            raise ValueError(f"Invalid length (expected: {64}, got: {len(address_no_prefix)})")

        return address_no_prefix
