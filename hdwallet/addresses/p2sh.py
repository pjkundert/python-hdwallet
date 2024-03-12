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
from ..const import PUBLIC_KEY_TYPES
from ..ecc import (
    IPublicKey, SLIP10Secp256k1PublicKey, validate_and_get_public_key
)
from ..cryptocurrencies import Bitcoin
from ..crypto import hash160
from ..utils import (
    get_bytes, integer_to_bytes, bytes_to_string
)
from .iaddress import IAddress


class P2SHAddress(IAddress):

    network_version: int = Bitcoin.NETWORKS.MAINNET.SCRIPT_ADDRESS_PREFIX
    alphabet: str = Bitcoin.PARAMS.ALPHABET

    @staticmethod
    def name() -> str:
        return "P2SH"

    @classmethod
    def encode(cls, public_key: Union[bytes, str, IPublicKey], **kwargs: Any) -> str:

        network_version: bytes = integer_to_bytes(
            kwargs.get("network_version", cls.network_version)
        )
        public_key: IPublicKey = validate_and_get_public_key(
            public_key=public_key, public_key_cls=SLIP10Secp256k1PublicKey
        )
        public_key_hash: bytes = hash160(
            public_key.raw_compressed()
            if kwargs.get("public_key_type", PUBLIC_KEY_TYPES.COMPRESSED) == PUBLIC_KEY_TYPES.COMPRESSED else
            public_key.raw_uncompressed()
        )
        script_hash: bytes = hash160(get_bytes(
            "76a914" + bytes_to_string(public_key_hash) + "88ac"
        ))

        return ensure_string(check_encode(
            (network_version + script_hash), alphabet=kwargs.get(
                "alphabet", cls.alphabet
            )
        ))

    @classmethod
    def decode(cls, address: str, **kwargs: Any) -> str:

        network_version: bytes = integer_to_bytes(
            kwargs.get("network_version", cls.network_version)
        )
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
