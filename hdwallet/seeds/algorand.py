#!/usr/bin/env python3

from ..mnemonics.algorand import AlgorandMnemonic
from . import ISeed


class AlgorandSeed(ISeed):

    @classmethod
    def generate(cls, mnemonic: str, **kwargs) -> str:

        if not AlgorandMnemonic.is_valid(mnemonic=mnemonic):
            ValueError("Invalid Algorand mnemonic words")

        return AlgorandMnemonic.decode(mnemonic=mnemonic)
