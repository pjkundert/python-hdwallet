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

    def __init__(self, seed: str, **kwargs) -> None:
        self._seed = seed

    @classmethod
    def name(cls) -> str:
        pass

    def seed(self) -> str:
        return self._seed

    @classmethod
    @abstractmethod
    def from_mnemonic(cls, mnemonic: str, **kwargs) -> str:
        pass
