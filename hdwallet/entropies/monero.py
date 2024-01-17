#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import List

from .ientropy import IEntropy


class MONERO_ENTROPY_STRENGTHS:

    ONE_HUNDRED_TWENTY_EIGHT: int = 128
    TWO_HUNDRED_FIFTY_SIX: int = 256


class MoneroEntropy(IEntropy):

    _name = "Monero"

    strengths = [
        MONERO_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT,
        MONERO_ENTROPY_STRENGTHS.TWO_HUNDRED_FIFTY_SIX
    ]
