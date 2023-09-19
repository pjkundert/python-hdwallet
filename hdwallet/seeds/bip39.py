#!/usr/bin/env python3

from typing import Optional

import unicodedata

from ..utils import bytes_to_string
from ..crypto import pbkdf2_hmac_sha512
from ..mnemonics.bip39 import BIP39Mnemonic
from . import ISeed


class BIP39Seed(ISeed):

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
