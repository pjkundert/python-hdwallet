#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Tuple

from .bip44 import BIP44Derivation


class BIP84Derivation(BIP44Derivation):  # https://github.com/bitcoin/bips/blob/master/bip-0084.mediawiki

    _purpose: Tuple[int, bool] = (84, True)

    @classmethod
    def name(cls) -> str:
        """
        Get the name of the derivation class.

        :return: The name of the derivation class.
        :rtype: str

        >>> from hdwallet.derivations.bip84 import BIP84Derivation
        >>> derivation: BIP84Derivation = BIP84Derivation(bip84="...")
        >>> derivation.name()
        "BIP84"
        """

        return "BIP84"
