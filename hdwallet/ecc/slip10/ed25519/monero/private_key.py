#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from nacl.signing import VerifyKey

from ....iecc import (
    IPublicKey, IPrivateKey
)
from .....libs.ed25519 import (
    scalar_is_valid, point_scalar_mul_base
)
from .. import SLIP10Ed25519PrivateKey
from .public_key import SLIP10Ed25519MoneroPublicKey


class SLIP10Ed25519MoneroPrivateKey(SLIP10Ed25519PrivateKey):

    @staticmethod
    def name() -> str:
        return "SLIP10-Ed25519-Monero"

    @classmethod
    def from_bytes(cls, private_key: bytes) -> IPrivateKey:
        if not scalar_is_valid(private_key):
            raise ValueError("Invalid private key bytes")
        return super().from_bytes(private_key)

    def public_key(self) -> IPublicKey:
        return SLIP10Ed25519MoneroPublicKey(
            VerifyKey(
                point_scalar_mul_base(bytes(self.signing_key))
            )
        )
