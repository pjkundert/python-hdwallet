#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Any
from nacl.signing import SigningKey
from nacl import exceptions

from ....const import SLIP10_ED25519_CONST
from ...iecc import (
    IPublicKey, IPrivateKey
)
from .public_key import SLIP10Ed25519PublicKey


class SLIP10Ed25519PrivateKey(IPrivateKey):

    signing_key: SigningKey

    def __init__(self, signing_key: SigningKey) -> None:
        self.signing_key = signing_key

    @staticmethod
    def name() -> str:
        return "SLIP10-Ed25519"

    @classmethod
    def from_bytes(cls, private_key: bytes) -> IPrivateKey:
        try:
            return cls(SigningKey(private_key))
        except (exceptions.RuntimeError, exceptions.ValueError) as ex:
            raise ValueError("Invalid private key bytes") from ex

    @staticmethod
    def length() -> int:
        return SLIP10_ED25519_CONST.PRIVATE_KEY_BYTE_LENGTH

    def underlying_object(self) -> Any:
        return self.signing_key

    def raw(self) -> bytes:
        return bytes(self.signing_key)

    def public_key(self) -> IPublicKey:
        return SLIP10Ed25519PublicKey(self.signing_key.verify_key)
