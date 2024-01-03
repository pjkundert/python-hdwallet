#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from abc import (
    ABC, abstractmethod
)


class ISeed(ABC):

    _name: str
    _seed: str

    def __init__(self, seed: str) -> None:
        self._seed = seed

    def name(self) -> str:
        return self._name

    def seed(self) -> str:
        return self._name

    @classmethod
    @abstractmethod
    def generate(cls, mnemonic: str) -> str:
        pass
