#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from ..point import SLIP10Ed25519Point


class SLIP10Ed25519MoneroPoint(SLIP10Ed25519Point):

    @staticmethod
    def name() -> str:
        """
        Get the name of the ecc class.

        :return: The name of the ecc class.
        :rtype: str

        >>> from hdwallet.ecc.slip10.ed25519.monero.point import SLIP10Ed25519MoneroPoint
        >>> ecc:  = SLIP10Ed25519MoneroPoint(point=...)
        >>> ecc.name()
        "SLIP10-Ed25519-Monero"
        """

        return "SLIP10-Ed25519-Monero"
