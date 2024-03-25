#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Union

from ..exceptions import MnemonicError
from ..mnemonics import (
    IMnemonic, MoneroMnemonic
)
from .iseed import ISeed


class MoneroSeed(ISeed):

    @classmethod
    def name(cls) -> str:
        return "Monero"

    @classmethod
    def from_mnemonic(cls, mnemonic: Union[str, IMnemonic], **kwargs) -> str:
        mnemonic = (
            mnemonic.mnemonic() if isinstance(mnemonic, IMnemonic) else mnemonic
        )
        if not MoneroMnemonic.is_valid(mnemonic=mnemonic):
            raise MnemonicError(f"Invalid {cls.name()} mnemonic words")

        return MoneroMnemonic.decode(mnemonic=mnemonic)
