#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    List, Union
)

import math

from ...utils import bytes_to_integer
from ..ientropy import IEntropy


class ELECTRUM_V2_ENTROPY_STRENGTHS:

    ONE_HUNDRED_THIRTY_TWO: int = 132
    TWO_HUNDRED_SIXTY_FOUR: int = 264


class ElectrumV2Entropy(IEntropy):

    _name = "Electrum-V2"

    strengths = [
        ELECTRUM_V2_ENTROPY_STRENGTHS.ONE_HUNDRED_THIRTY_TWO,
        ELECTRUM_V2_ENTROPY_STRENGTHS.TWO_HUNDRED_SIXTY_FOUR
    ]

    @classmethod
    def is_valid_strength(cls, strength: int) -> bool:
        for _strength in cls.strengths:
            if _strength - 11 <= strength <= _strength:
                return True
        return False

    @classmethod
    def are_entropy_bits_enough(cls, entropy: Union[bytes, int]) -> bool:

        if isinstance(entropy, bytes):
            entropy: int = bytes_to_integer(entropy)

        entropy_strength: int = 0 if entropy <= 0 else math.floor(math.log(entropy, 2))
        return cls.is_valid_strength(entropy_strength)
