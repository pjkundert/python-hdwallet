#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Any, Union
)

from ..libs.base58 import (
    ensure_string, check_encode, check_decode
)
from ..ecc import (
    IPublicKey, SLIP10Secp256k1PublicKey, validate_and_get_public_key
)
from ..cryptocurrencies import Tron
from ..crypto import kekkak256
from ..utils import (
    integer_to_bytes, bytes_to_string
)
from .iaddress import IAddress


class TronAddress(IAddress):

    public_key_address_prefix: int = Tron.NETWORKS.MAINNET.PUBLIC_KEY_ADDRESS_PREFIX
    alphabet: str = Tron.PARAMS.ALPHABET

    @staticmethod
    def name() -> str:
        return "Tron"

    @classmethod
    def encode(cls, public_key: Union[bytes, str, IPublicKey], **kwargs: Any) -> str:

        network_version: bytes = integer_to_bytes(cls.public_key_address_prefix)
        
        public_key: IPublicKey = validate_and_get_public_key(
            public_key=public_key, public_key_cls=SLIP10Secp256k1PublicKey
        )
        
        address: str = bytes_to_string(
            kekkak256(public_key.raw_uncompressed()[1:])
        )[24:]

        return ensure_string(check_encode(
            (network_version + bytearray.fromhex(address)), alphabet=kwargs.get(
                "alphabet", cls.alphabet
            )
        ))

    @classmethod
    def decode(cls, address: str, **kwargs: Any) -> str:
        
        network_version: bytes = integer_to_bytes(cls.public_key_address_prefix)
        
        address_decode: bytes = check_decode(
            address, alphabet=kwargs.get(
                "alphabet", cls.alphabet
            )
        )

        expected_length: int = 20 + len(network_version)
        if len(address_decode) != expected_length:
            raise ValueError(f"Invalid length (expected: {expected_length}, got: {len(address_decode)})")

        prefix_got: bytes = address_decode[:len(network_version)]
        if network_version != prefix_got:
            raise ValueError(f"Invalid prefix (expected: {network_version}, got: {prefix_got})")

        return bytes_to_string(address_decode[len(network_version):])
