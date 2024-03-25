#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Optional, Union
)

import unicodedata

from ...crypto import pbkdf2_hmac_sha512
from ...exceptions import MnemonicError
from ...utils import bytes_to_string
from ...mnemonics import (
    IMnemonic, ElectrumV2Mnemonic
)
from ..iseed import ISeed


class ElectrumV2Seed(ISeed):

    seed_salt_modifier: str = "electrum"
    seed_pbkdf2_rounds: int = 2048

    @classmethod
    def name(cls) -> str:
        return "Electrum-V2"

    @classmethod
    def from_mnemonic(cls, mnemonic: Union[str, IMnemonic], passphrase: Optional[str] = None) -> str:
        mnemonic = (
            mnemonic.mnemonic() if isinstance(mnemonic, IMnemonic) else mnemonic
        )
        if not ElectrumV2Mnemonic.is_valid(mnemonic=mnemonic):
            raise MnemonicError(f"Invalid {cls.name()} mnemonic words")

        salt: str = unicodedata.normalize("NFKD", (
            (cls.seed_salt_modifier + passphrase) if passphrase else cls.seed_salt_modifier
        ))
        return bytes_to_string(pbkdf2_hmac_sha512(
            password=mnemonic, salt=salt, iteration_num=cls.seed_pbkdf2_rounds
        ))
