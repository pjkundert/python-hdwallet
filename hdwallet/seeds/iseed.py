#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from abc import (
    ABC, abstractmethod
)


class ISeed(ABC):

    @classmethod
    @abstractmethod
    def generate(cls, mnemonic: str, **kwargs) -> str:
        pass
