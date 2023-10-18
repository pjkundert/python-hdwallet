#!/usr/bin/env python3

# Copyright © 2020-2023, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import List

from .. import IEntropy


class ELECTRUM_V1_ENTROPY_LENGTHS:

    ONE_HUNDRED_TWENTY_EIGHT: int = 128


class ElectrumV1Entropy(IEntropy):

    lengths: List[int] = [
        ELECTRUM_V1_ENTROPY_LENGTHS.ONE_HUNDRED_TWENTY_EIGHT
    ]
