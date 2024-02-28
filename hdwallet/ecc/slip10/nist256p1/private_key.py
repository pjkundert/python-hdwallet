#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Any
from ecdsa import SigningKey
from ecdsa import (
    curves, keys
)

from ....const import SLIP10_SECP256K1_CONST
from ...iecc import (
    IPublicKey, IPrivateKey
)
from .public_key import SLIP10Nist256p1PublicKey


class SLIP10Nist256p1PrivateKey(IPrivateKey):
    
    signing_key: SigningKey

    def __init__(self, signing_key: SigningKey) -> None:
        self.signing_key = signing_key

    @staticmethod
    def name() -> str:
        return "SLIP10-Nist256p1"

    @classmethod
    def from_bytes(cls, private_key: bytes) -> IPrivateKey:
        try:
            return cls(
                SigningKey.from_string(
                    private_key, curve=curves.NIST256p
                )
            )
        except keys.MalformedPointError as ex:
            raise ValueError("Invalid private key bytes") from ex

    @staticmethod
    def length() -> int:
        return SLIP10_SECP256K1_CONST.PRIVATE_KEY_BYTE_LENGTH

    def underlying_object(self) -> Any:
        return self.signing_key

    def raw(self) -> bytes:
        return self.signing_key.to_string()

    def public_key(self) -> IPublicKey:
        return SLIP10Nist256p1PublicKey(self.signing_key.get_verifying_key())
