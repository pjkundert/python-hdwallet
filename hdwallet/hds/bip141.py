#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from ..addresses.p2wpkh import P2WPKHAddress
from ..addresses.p2wpkh_in_p2sh import P2WPKHInP2SHAddress
from ..addresses.p2wsh import P2WSHAddress
from ..addresses.p2wpkh_in_p2sh import P2WPKHInP2SHAddress
from .bip32 import BIP32HD


class BIP141HD(BIP32HD):

    @classmethod
    def name(cls) -> str:
        return "BIP141"

    def address(self, **kwargs) -> str:
        pass
