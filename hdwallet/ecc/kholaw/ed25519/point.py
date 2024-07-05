#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from ...slip10.ed25519 import SLIP10Ed25519Point


class KholawEd25519Point(SLIP10Ed25519Point):

    @staticmethod
    def name() -> str:
        """
        Get the name of the ecc class.

        :return: The name of the ecc class.
        :rtype: str

        >>> from hdwallet.ecc.kholaw.ed25519.point import KholawEd25519Point
        >>> ecc:  = KholawEd25519Point(point=...)
        >>> ecc.name()
        "Kholaw-Ed25519"
        """

        return "Kholaw-Ed25519"
