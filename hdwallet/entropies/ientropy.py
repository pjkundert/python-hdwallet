#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    List, Union
)

import secrets
import os

from ..utils import (
    get_bytes, integer_to_bytes, bytes_to_string
)


class IEntropy:

    _entropy: str
    _strength: int

    strengths: List[int]

    def __init__(self, entropy: Union[bytes, str]) -> None:
        try:
            strength: int = len(get_bytes(entropy))
            if not self.is_valid_bytes_strength(strength):
                raise Exception("Unsupported entropy strength")
            self._entropy = bytes_to_string(entropy)
            self._strength = strength * 8
        except ValueError:
            raise Exception("Invalid entropy data")

    @classmethod
    def name(cls) -> str:
        pass

    def entropy(self) -> str:
        return self._entropy

    def strength(self) -> int:
        return self._strength

    @classmethod
    def generate(cls, strength: int) -> str:
        return bytes_to_string(
            os.urandom(strength // 8)
            if strength % 8 == 0 else
            integer_to_bytes(
                secrets.randbits(strength)
            )
        )

    @classmethod
    def is_valid_strength(cls, strength: int) -> bool:
        return strength in cls.strengths

    @classmethod
    def is_valid_bytes_strength(cls, bytes_strength: int) -> bool:
        return cls.is_valid_strength(bytes_strength * 8)
