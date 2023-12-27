#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import List

import secrets
import os

from ..utils import (
    integer_to_bytes, bytes_to_string
)


class IEntropy:

    lengths: List[int]

    @classmethod
    def generate(cls, length: int) -> str:
        return bytes_to_string(
            os.urandom(length // 8)
            if length % 8 == 0 else
            integer_to_bytes(
                secrets.randbits(length)
            )
        )

    @classmethod
    def is_valid_length(cls, length: int) -> bool:
        return length in cls.lengths

    @classmethod
    def is_valid_bytes_length(cls, bytes_length: int) -> bool:
        return cls.is_valid_length(bytes_length * 8)
