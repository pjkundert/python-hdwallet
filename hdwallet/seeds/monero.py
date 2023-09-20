#!/usr/bin/env python3

from ..mnemonics.monero import MoneroMnemonic
from . import ISeed


class MoneroSeed(ISeed):

    @classmethod
    def generate(cls, mnemonic: str) -> str:

        if not MoneroMnemonic.is_valid(mnemonic=mnemonic):
            ValueError("Invalid Monero mnemonic words")

        return MoneroMnemonic.decode(mnemonic=mnemonic)
