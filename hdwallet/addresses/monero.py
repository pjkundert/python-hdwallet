#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Tuple, Union, Optional, Dict
)

from ..libs.base58 import (
    encode_monero, decode_monero
)
from ..ecc import (
    IPublicKey, SLIP10Ed25519MoneroPublicKey, validate_and_get_public_key
)
from ..cryptocurrencies.monero import (
    Mainnet, Stagenet, Testnet
)
from ..crypto import kekkak256
from ..utils import (
    bytes_to_string, integer_to_bytes
)


class MoneroAddress:

    checksum_length: int = 4
    payment_id_length: int = 8
    network_types: Dict[str, Dict[str, Dict[str, int]]] = {
        "mainnet": {
            "version_types": {
                "standard": Mainnet.STANDARD, "integrated": Mainnet.INTEGRATED, "sub-address": Mainnet.SUB_ADDRESS
            }
        },
        "stagenet": {
            "version_types": {
                "standard": Stagenet.STANDARD, "integrated": Stagenet.INTEGRATED, "sub-address": Stagenet.SUB_ADDRESS
            }
        },
        "testnet": {
            "version_types": {
                "standard": Testnet.STANDARD, "integrated": Testnet.INTEGRATED, "sub-address": Testnet.SUB_ADDRESS
            }
        }
    }

    @staticmethod
    def name() -> str:
        return "Monero"

    @classmethod
    def compute_checksum(cls, public_key: bytes) -> bytes:
        return kekkak256(public_key)[:cls.checksum_length]

    @classmethod
    def encode(
        cls,
        spend_public_key: Union[bytes, str, IPublicKey],
        view_public_key: Union[bytes, str, IPublicKey],
        network_type: str = "mainnet",
        version_type: str = "standard",
        payment_id: Optional[bytes] = None
    ) -> str:

        spend_public_key: IPublicKey = validate_and_get_public_key(
            public_key=spend_public_key, public_key_cls=SLIP10Ed25519MoneroPublicKey
        )
        view_public_key: IPublicKey = validate_and_get_public_key(
            public_key=view_public_key, public_key_cls=SLIP10Ed25519MoneroPublicKey
        )

        if payment_id is not None and len(payment_id) != cls.payment_id_length:
            raise ValueError("Invalid payment ID length")

        version: bytes = integer_to_bytes(
            cls.network_types[network_type]["version_types"][version_type]
        )
        payload: bytes = (
            version + spend_public_key.raw_compressed() +
            view_public_key.raw_compressed() +
            (b"" if payment_id is None else payment_id)
        )

        return encode_monero(payload + cls.compute_checksum(payload))

    @classmethod
    def decode(
        cls,
        address: str,
        network_type: str = "mainnet",
        version_type: str = "standard",
        payment_id: Optional[bytes] = None
    ) -> Tuple[str, str]:

        address_decode: bytes = decode_monero(address)

        checksum: bytes = address_decode[-1 * cls.checksum_length:]
        payload_with_prefix: bytes = address_decode[:-1 * cls.checksum_length]

        checksum_got: bytes = cls.compute_checksum(payload_with_prefix)
        if checksum != checksum_got:
            raise ValueError(f"Invalid checksum (expected: {bytes_to_string(checksum)}, got: {bytes_to_string(checksum_got)})")

        version: bytes = integer_to_bytes(
            cls.network_types[network_type]["version_types"][version_type]
        )
        version_got = payload_with_prefix[:len(version)]
        if version != version_got:
            raise ValueError(f"Invalid version (expected: {version}, got: {version_got})")

        payload_without_prefix: bytes = payload_with_prefix[len(version):]

        expected_length: int = SLIP10Ed25519MoneroPublicKey.compressed_length() * 2
        try:
            if len(payload_without_prefix) != expected_length:
                raise ValueError(f"Invalid length (expected: {expected_length}, got: {len(payload_without_prefix)})")
        except ValueError as ex:
            if len(payload_without_prefix) != expected_length + cls.payment_id_length:
                raise ValueError(f"Invalid length (expected: {expected_length + cls.payment_id_length}, got: {len(payload_without_prefix)})")

            if payment_id is None or len(payment_id) != cls.payment_id_length:
                raise ValueError("Invalid payment ID")

            payment_id_got_bytes = payload_without_prefix[-cls.payment_id_length:]
            if payment_id != payment_id_got_bytes:
                raise ValueError(f"Invalid payment ID (expected: {bytes_to_string(payment_id_got_bytes)}, got: {bytes_to_string(payment_id_got_bytes)})")

        length: int = SLIP10Ed25519MoneroPublicKey.compressed_length()

        spend_public_key: bytes = payload_without_prefix[:length]
        if not SLIP10Ed25519MoneroPublicKey.is_valid_bytes(spend_public_key):
            raise ValueError(f"Invalid {SLIP10Ed25519MoneroPublicKey.name()} public key {bytes_to_string(spend_public_key)}")

        view_public_key: bytes = payload_without_prefix[length:(length * 2)]
        if not SLIP10Ed25519MoneroPublicKey.is_valid_bytes(view_public_key):
            raise ValueError(f"Invalid {SLIP10Ed25519MoneroPublicKey.name()} public key {bytes_to_string(view_public_key)}")

        return bytes_to_string(spend_public_key), bytes_to_string(view_public_key)
