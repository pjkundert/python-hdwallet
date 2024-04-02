#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from abc import (
    ABC, abstractmethod
)
from typing import (
    Union, Optional
)

from ..mnemonics import IMnemonic


class ISeed(ABC):

    _name: str
    _seed: str
    _passphrase: Optional[str]
    _mnemonic_type: Optional[str]
    _cardano_type: Optional[str]

    def __init__(self, seed: str, **kwargs) -> None:
        self._seed = seed
        self._passphrase = kwargs.get("passphrase", None)
        self._mnemonic_type = kwargs.get("mnemonic_type", None)
        self._cardano_type = kwargs.get("cardano_type", None)

    @classmethod
    def name(cls) -> str:
        pass

    def seed(self) -> str:
        return self._seed

    def passphrase(self) -> Optional[str]:
        return self._passphrase

    def cardano_type(self) -> Optional[str]:
        return self._cardano_type

    def mnemonic_type(self) -> Optional[str]:
        return self._mnemonic_type

    @classmethod
    @abstractmethod
    def from_mnemonic(cls, mnemonic: Union[str, IMnemonic]) -> str:
        pass
