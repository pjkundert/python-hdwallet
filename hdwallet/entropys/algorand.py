#!/usr/bin/env python3

from typing import List

from . import IEntropy


class ALGORAND_ENTROPY_LENGTHS:

    TWO_HUNDRED_FIFTY_SIX: int = 256


class AlgorandEntropy(IEntropy):

    lengths: List[int] = [
        ALGORAND_ENTROPY_LENGTHS.TWO_HUNDRED_FIFTY_SIX
    ]
