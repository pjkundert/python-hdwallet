#!/usr/bin/env python3

# Copyright © 2020-2023, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    List, Union
)

import math

from ...utils import bytes_to_integer
from ...mnemonics.bip39 import BIP39Mnemonic
from ..ientropy import IEntropy


class ELECTRUM_V2_ENTROPY_LENGTHS:

    ONE_HUNDRED_THIRTY_TWO: int = 132
    TWO_HUNDRED_SIXTY_FOUR: int = 264


class ElectrumV2Entropy(IEntropy):

    lengths: List[int] = [
        ELECTRUM_V2_ENTROPY_LENGTHS.ONE_HUNDRED_THIRTY_TWO,
        ELECTRUM_V2_ENTROPY_LENGTHS.TWO_HUNDRED_SIXTY_FOUR
    ]

    @classmethod
    def is_valid_length(cls, length: int) -> bool:
        for _length in cls.lengths:
            if _length - BIP39Mnemonic.word_bit_length <= length <= _length:
                return True
        return False

    @classmethod
    def are_entropy_bits_enough(cls, entropy: Union[bytes, int]) -> bool:

        if isinstance(entropy, bytes):
            entropy: int = bytes_to_integer(entropy)

        entropy_length: int = 0 if entropy <= 0 else math.floor(math.log(entropy, 2))
        return cls.is_valid_length(entropy_length)
