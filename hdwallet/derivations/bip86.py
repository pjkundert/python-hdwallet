#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Tuple

from .bip44 import BIP44Derivation


class BIP86Derivation(BIP44Derivation):  # https://github.com/bitcoin/bips/blob/master/bip-0086.mediawiki

    _purpose: Tuple[int, bool] = (86, True)

    @classmethod
    def name(cls) -> str:
        """
        Get the name of the derivation class.

        :return: The name of the derivation class.
        :rtype: str

        >>> from hdwallet.derivations.bip86 import BIP86Derivation
        >>> derivation: BIP86Derivation = BIP86Derivation(bip86="...")
        >>> derivation.name()
        "BIP86"
        """

        return "BIP86"
