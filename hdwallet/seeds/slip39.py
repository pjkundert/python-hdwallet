#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Optional, Union
)

import unicodedata

from ..crypto import pbkdf2_hmac_sha512
from ..exceptions import MnemonicError
from ..utils import bytes_to_string
from ..mnemonics import (
    IMnemonic, BIP39Mnemonic
)
from .iseed import ISeed


class SLP39Seed(ISeed):
    """This class transmits the seed collected from SLIP-39 recovery.  This entropy is used directly
    to produce hierarchical deterministic wallets, unlike for BIP39, where the original entropy is
    hashed and extended to 512 bits before being used.  The 3 valid seed sizes are 128, 256 and 512
    bits.

    Once recovered from SLIP-39 encoding, the seed data is provided and presented as simple hex.

    .. note::
        This class inherits from the ``ISeed`` class, thereby ensuring that all functions are accessible.

    """
    @classmethod
    def name(cls) -> str:
        """
        Get the name of the seeds class.

        :return: The name of the seeds class.
        :rtype: str
        """

        return "SLIP39"

    @classmethod
    def from_mnemonic(cls, mnemonic: Union[str, IMnemonic], passphrase: Optional[str] = None) -> str:
        """
        Converts a mnemonic phrase to its corresponding seed.

        The Mnemonic representation for SLIP-39 seeds is simple hex.  SLIP-39 seeds may be encrypted by
        their own passphrase; this passphrase is the BIP-39 seed passphrase.

        :param mnemonic: The mnemonic phrase to be decoded. Can be a string or an instance of `IMnemonic`.
        :type mnemonic: Union[str, IMnemonic]

        :param passphrase: An optional passphrase used for additional security when decoding the mnemonic phrase.
        :type passphrase: Optional[str]

        :return: The decoded seed as a string.
        :rtype: str
        """

        mnemonic = (
            mnemonic.mnemonic() if isinstance(mnemonic, IMnemonic) else mnemonic
        )
        if not BIP39Mnemonic.is_valid(mnemonic=mnemonic):
            raise MnemonicError(f"Invalid {cls.name()} mnemonic words")

        salt: str = unicodedata.normalize("NFKD", (
            (cls.seed_salt_modifier + passphrase) if passphrase else cls.seed_salt_modifier
        ))
        return bytes_to_string(pbkdf2_hmac_sha512(
            password=mnemonic, salt=salt, iteration_num=cls.seed_pbkdf2_rounds
        ))
