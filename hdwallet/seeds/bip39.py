#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Optional

import unicodedata

from ..utils import bytes_to_string
from ..crypto import pbkdf2_hmac_sha512
from ..mnemonics.bip39 import BIP39Mnemonic
from .iseed import ISeed


class BIP39Seed(ISeed):

    _name = "BIP39"

    # Salt modifier for seed generation
    seed_salt_modifier: str = "mnemonic"
    # PBKDF2 round for seed generation
    seed_pbkdf2_rounds: int = 2048

    @classmethod
    def generate(cls, mnemonic: str, passphrase: Optional[str] = None) -> str:

        if not BIP39Mnemonic.is_valid(mnemonic=mnemonic):
            ValueError("Invalid BIP39 mnemonic words")

        salt: str = unicodedata.normalize("NFKD", (
            (cls.seed_salt_modifier + passphrase) if passphrase else cls.seed_salt_modifier
        ))
        return bytes_to_string(pbkdf2_hmac_sha512(
            password=mnemonic, salt=salt, iteration_num=cls.seed_pbkdf2_rounds
        ))
