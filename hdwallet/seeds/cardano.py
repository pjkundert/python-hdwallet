#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Optional

import cbor2

from ..utils import (
    get_bytes, bytes_to_string
)
from ..crypto import blake2b_256
from ..mnemonics.bip39 import BIP39Mnemonic
from . import (
    ISeed, BIP39Seed
)


class CardanoSeed(ISeed):

    _cardano_type: str = "byron-icarus"
    _cardano_types: list = [
        "byron-icarus", "byron-ledger", "byron-legacy", "shelley-icarus", "shelley-ledger"
    ]

    def __init__(self, seed: str, cardano_type: str = "byron-icarus", **kwargs) -> None:
        super(CardanoSeed, self).__init__(seed, **kwargs)

        if cardano_type not in self._cardano_types:
            raise ValueError(f"Invalid Cardano type (expected: {self._cardano_types}, got: {cardano_type!r})")

        self._cardano_type = cardano_type
        self._seed = seed

    @classmethod
    def name(cls) -> str:
        return "Cardano"

    def cardano_type(self) -> str:
        return self._cardano_type

    @classmethod
    def generate(cls, mnemonic: str, cardano_type: str = "byron-icarus", **kwargs) -> str:

        if cardano_type == "byron-icarus":
            return cls.generate_byron_icarus(mnemonic=mnemonic)
        if cardano_type == "byron-ledger":
            return cls.generate_byron_ledger(
                mnemonic=mnemonic, passphrase=kwargs.get("passphrase", None)
            )
        if cardano_type == "byron-legacy":
            return cls.generate_byron_legacy(mnemonic=mnemonic)
        if cardano_type == "shelley-icarus":
            return cls.generate_shelley_icarus(mnemonic=mnemonic)
        elif cardano_type == "shelley-ledger":
            return cls.generate_shelley_ledger(
                mnemonic=mnemonic, passphrase=kwargs.get("passphrase", None)
            )
        else:
            raise ValueError(f"Invalid Cardano type (expected: {cls._cardano_types}, got: {cardano_type!r})")

    @classmethod
    def generate_byron_icarus(cls, mnemonic: str) -> str:

        if not BIP39Mnemonic.is_valid(mnemonic=mnemonic):
            ValueError("Invalid BIP39 mnemonic words")

        return BIP39Mnemonic.decode(mnemonic=mnemonic)

    @classmethod
    def generate_byron_ledger(cls, mnemonic: str, passphrase: Optional[str] = None) -> str:
        return BIP39Seed.generate(mnemonic=mnemonic, passphrase=passphrase)

    @classmethod
    def generate_byron_legacy(cls, mnemonic: str) -> str:

        if not BIP39Mnemonic.is_valid(mnemonic=mnemonic):
            ValueError("Invalid BIP39 mnemonic words")

        return bytes_to_string(blake2b_256(
            cbor2.dumps(get_bytes(BIP39Mnemonic.decode(mnemonic=mnemonic)))
        ))

    @classmethod
    def generate_shelley_icarus(cls, mnemonic: str) -> str:
        return cls.generate_byron_icarus(
            mnemonic=mnemonic
        )

    @classmethod
    def generate_shelley_ledger(cls, mnemonic: str, passphrase: Optional[str] = None) -> str:
        return cls.generate_byron_ledger(
            mnemonic=mnemonic, passphrase=passphrase
        )
