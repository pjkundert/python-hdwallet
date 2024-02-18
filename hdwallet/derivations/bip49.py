#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Tuple

from .bip44 import BIP44Derivation


class BIP49Derivation(BIP44Derivation):  # https://github.com/bitcoin/bips/blob/master/bip-0049.mediawiki

    _purpose: Tuple[int, bool] = (49, True)

    @classmethod
    def name(cls) -> str:
        return "BIP49"
