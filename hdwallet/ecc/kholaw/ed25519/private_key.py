#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Any
from nacl import signing

from ....const import KHOLAW_ED25519_CONST
from ....libs.ed25519 import point_scalar_mul_base
from ...slip10.ed25519 import SLIP10Ed25519PrivateKey
from ...iecc import (
    IPublicKey, IPrivateKey
)
from .public_key import KholawEd25519PublicKey


class KholawEd25519PrivateKey(IPrivateKey):

    m_sign_key: IPrivateKey
    m_ext_key: bytes

    def __init__(self, key_obj: IPrivateKey, key_ex_bytes: bytes) -> None:
        if not isinstance(key_obj, SLIP10Ed25519PrivateKey):
            raise TypeError("Invalid private key object type")
        if len(key_ex_bytes) != SLIP10Ed25519PrivateKey.length():
            raise ValueError("Invalid extended key length")

        self.m_sign_key = key_obj
        self.m_ext_key = key_ex_bytes

    @staticmethod
    def name() -> str:
        return "Kholaw-Ed25519"

    @classmethod
    def from_bytes(cls, key_bytes: bytes) -> IPrivateKey:
        return cls(
            SLIP10Ed25519PrivateKey.from_bytes(
                key_bytes[:SLIP10Ed25519PrivateKey.length()]
            ),
            key_bytes[SLIP10Ed25519PrivateKey.length():]
        )

    @staticmethod
    def length() -> int:
        return KHOLAW_ED25519_CONST.PRIVATE_KEY_BYTE_LENGTH

    def underlying_object(self) -> Any:
        return self.m_sign_key.underlying_object()

    def raw(self) -> bytes:
        return self.m_sign_key.raw() + self.m_ext_key

    def public_key(self) -> IPublicKey:
        return KholawEd25519PublicKey(
            signing.VerifyKey(
                point_scalar_mul_base(bytes(self.m_sign_key.underlying_object()))
            )
        )
