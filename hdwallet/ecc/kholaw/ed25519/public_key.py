#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from ...slip10.ed25519 import SLIP10Ed25519PublicKey
from ...iecc import IPoint
from .point import KholawEd25519Point


class KholawEd25519PublicKey(SLIP10Ed25519PublicKey):

    @staticmethod
    def name() -> str:
        return "Kholaw-Ed25519"

    def point(self) -> IPoint:
        return KholawEd25519Point(bytes(self.verify_key))

