#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from .....const import SLIP10_ED25519_CONST
from ....iecc import IPoint
from .. import SLIP10Ed25519PublicKey
from .point import SLIP10Ed25519MoneroPoint


class SLIP10Ed25519MoneroPublicKey(SLIP10Ed25519PublicKey):

    @staticmethod
    def name() -> str:
        return "SLIP10-Ed25519-Monero"

    @staticmethod
    def compressed_length() -> int:
        return SLIP10_ED25519_CONST.PUBLIC_KEY_BYTE_LENGTH

    @staticmethod
    def uncompressed_length() -> int:
        return SLIP10Ed25519MoneroPublicKey.compressed_length()

    def raw_compressed(self) -> bytes:
        return bytes(self.verify_key)

    def raw_uncompressed(self) -> bytes:
        return self.raw_compressed()

    def point(self) -> IPoint:
        return SLIP10Ed25519MoneroPoint(bytes(self.verify_key))
