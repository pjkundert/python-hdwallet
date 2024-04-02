#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Optional, Union
)

import cbor2

from ..mnemonics import (
    IMnemonic, BIP39Mnemonic
)
from ..cryptocurrencies import Cardano
from ..crypto import blake2b_256
from ..exceptions import (
    Error, MnemonicError
)
from ..utils import (
    get_bytes, bytes_to_string
)
from . import (
    ISeed, BIP39Seed
)


class CardanoSeed(ISeed):

    _cardano_type: str

    def __init__(
        self, seed: str, cardano_type: str = Cardano.TYPES.BYRON_ICARUS, passphrase: Optional[str] = None
    ) -> None:
        super(CardanoSeed, self).__init__(
            seed=seed, cardano_type=cardano_type, passphrase=passphrase
        )

        if cardano_type not in Cardano.TYPES.get_cardano_types():
            raise Error(
                "Invalid Cardano type", expected=Cardano.TYPES.get_cardano_types(), got=cardano_type
            )

        self._cardano_type = cardano_type
        self._seed = seed

    @classmethod
    def name(cls) -> str:
        return "Cardano"

    def cardano_type(self) -> str:
        return self._cardano_type

    @classmethod
    def from_mnemonic(
        cls,
        mnemonic: Union[str, IMnemonic],
        passphrase: Optional[str] = None,
        cardano_type: str = Cardano.TYPES.BYRON_ICARUS
    ) -> str:

        if cardano_type == Cardano.TYPES.BYRON_ICARUS:
            return cls.generate_byron_icarus(mnemonic=mnemonic)
        if cardano_type == Cardano.TYPES.BYRON_LEDGER:
            return cls.generate_byron_ledger(
                mnemonic=mnemonic, passphrase=passphrase
            )
        if cardano_type == Cardano.TYPES.BYRON_LEGACY:
            return cls.generate_byron_legacy(mnemonic=mnemonic)
        if cardano_type == Cardano.TYPES.SHELLEY_ICARUS:
            return cls.generate_shelley_icarus(mnemonic=mnemonic)
        elif cardano_type == Cardano.TYPES.SHELLEY_LEDGER:
            return cls.generate_shelley_ledger(
                mnemonic=mnemonic, passphrase=passphrase
            )
        raise Error(
            "Invalid Cardano type", expected=Cardano.TYPES.get_cardano_types(), got=cardano_type
        )

    @classmethod
    def generate_byron_icarus(cls, mnemonic: Union[str, IMnemonic]) -> str:

        mnemonic = (
            mnemonic.mnemonic()
            if isinstance(mnemonic, IMnemonic) else
            mnemonic
        )
        if not BIP39Mnemonic.is_valid(mnemonic=mnemonic):
            raise MnemonicError(f"Invalid {BIP39Mnemonic.name()} mnemonic words")

        return BIP39Mnemonic.decode(mnemonic=mnemonic)

    @classmethod
    def generate_byron_ledger(cls, mnemonic: Union[str, IMnemonic], passphrase: Optional[str] = None) -> str:
        mnemonic = (
            mnemonic.mnemonic()
            if isinstance(mnemonic, IMnemonic) else
            mnemonic
        )
        return BIP39Seed.from_mnemonic(mnemonic=mnemonic, passphrase=passphrase)

    @classmethod
    def generate_byron_legacy(cls, mnemonic: Union[str, IMnemonic]) -> str:

        mnemonic = (
            mnemonic.mnemonic()
            if isinstance(mnemonic, IMnemonic) else
            mnemonic
        )
        if not BIP39Mnemonic.is_valid(mnemonic=mnemonic):
            raise MnemonicError(f"Invalid {BIP39Mnemonic.name()} mnemonic words")

        return bytes_to_string(blake2b_256(
            cbor2.dumps(get_bytes(BIP39Mnemonic.decode(mnemonic=mnemonic)))
        ))

    @classmethod
    def generate_shelley_icarus(cls, mnemonic: Union[str, IMnemonic]) -> str:
        return cls.generate_byron_icarus(
            mnemonic=mnemonic
        )

    @classmethod
    def generate_shelley_ledger(cls, mnemonic: str, passphrase: Optional[str] = None) -> str:
        return cls.generate_byron_ledger(
            mnemonic=mnemonic, passphrase=passphrase
        )
