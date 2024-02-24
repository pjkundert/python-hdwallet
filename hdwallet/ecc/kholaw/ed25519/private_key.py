#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Any
from nacl.signing import VerifyKey

from ....const import KHOLAW_ED25519_CONST
from ....libs.ed25519 import point_scalar_mul_base
from ...slip10.ed25519 import SLIP10Ed25519PrivateKey
from ...iecc import (
    IPublicKey, IPrivateKey
)
from .public_key import KholawEd25519PublicKey


class KholawEd25519PrivateKey(IPrivateKey):

    signing_key: IPrivateKey
    extended_key: bytes

    def __init__(self, private_key: IPrivateKey, extended_key: bytes) -> None:
        if not isinstance(private_key, SLIP10Ed25519PrivateKey):
            raise TypeError("Invalid private key object type")
        if len(extended_key) != SLIP10Ed25519PrivateKey.length():
            raise ValueError("Invalid extended key length")

        self.signing_key = private_key
        self.extended_key = extended_key

    @staticmethod
    def name() -> str:
        return "Kholaw-Ed25519"

    @classmethod
    def from_bytes(cls, private_key: bytes) -> IPrivateKey:
        return cls(
            SLIP10Ed25519PrivateKey.from_bytes(
                private_key[:SLIP10Ed25519PrivateKey.length()]
            ),
            private_key[SLIP10Ed25519PrivateKey.length():]
        )

    @staticmethod
    def length() -> int:
        return KHOLAW_ED25519_CONST.PRIVATE_KEY_BYTE_LENGTH

    def underlying_object(self) -> Any:
        return self.signing_key.underlying_object()

    def raw(self) -> bytes:
        return self.signing_key.raw() + self.extended_key

    def public_key(self) -> IPublicKey:
        return KholawEd25519PublicKey(VerifyKey(
            point_scalar_mul_base(bytes(self.signing_key.underlying_object()))
        ))
