#!/usr/bin/env python3

from typing import List

from . import IEntropy


class MONERO_ENTROPY_LENGTHS:

    ONE_HUNDRED_TWENTY_EIGHT: int = 128
    TWO_HUNDRED_FIFTY_SIX: int = 256


class MoneroEntropy(IEntropy):

    lengths: List[int] = [
        MONERO_ENTROPY_LENGTHS.ONE_HUNDRED_TWENTY_EIGHT,
        MONERO_ENTROPY_LENGTHS.TWO_HUNDRED_FIFTY_SIX
    ]
