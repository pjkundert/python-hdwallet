#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Any
from ed25519_blake2b import SigningKey

from .....const import SLIP10_ED25519_CONST
from ....iecc import (
    IPublicKey, IPrivateKey
)
from .public_key import SLIP10Ed25519Blake2bPublicKey


class SLIP10Ed25519Blake2bPrivateKey(IPrivateKey):

    signing_key: SigningKey

    def __init__(self, signing_key: SigningKey) -> None:
        self.signing_key = signing_key

    @staticmethod
    def name() -> str:
        return "SLIP10-Ed25519-Blake2b"

    @classmethod
    def from_bytes(cls, private_key: bytes) -> IPrivateKey:
        try:
            return cls(SigningKey(private_key))
        except ValueError as ex:
            raise ValueError("Invalid private key bytes") from ex

    @staticmethod
    def length() -> int:
        return SLIP10_ED25519_CONST.PRIVATE_KEY_BYTE_LENGTH

    def underlying_object(self) -> Any:
        return self.signing_key

    def raw(self) -> bytes:
        return self.signing_key.to_bytes()

    def public_key(self) -> IPublicKey:
        return SLIP10Ed25519Blake2bPublicKey(self.signing_key.get_verifying_key())
