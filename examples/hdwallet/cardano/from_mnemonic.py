#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.mnemonics import (
    BIP39Mnemonic, MONERO_MNEMONIC_WORDS, BIP39_MNEMONIC_LANGUAGES
)
from hdwallet.cryptocurrencies import Cardano as Cryptocurrency
from hdwallet.hds import CardanoHD
from hdwallet.derivations import (
    CIP1852Derivation, ROLES
)

import json


hdwallet: HDWallet = HDWallet(
    cryptocurrency=Cryptocurrency,
    hd=CardanoHD,
    cardano_type=Cryptocurrency.TYPES.SHELLEY_ICARUS,
    address_type=Cryptocurrency.ADDRESS_TYPES.STAKING,
    passphrase="meherett"
).from_mnemonic(
    mnemonic=BIP39Mnemonic(
        mnemonic=BIP39Mnemonic.from_words(
            words=MONERO_MNEMONIC_WORDS.TWELVE,
            language=BIP39_MNEMONIC_LANGUAGES.ITALIAN
        )
    )
).from_derivation(
    derivation=CIP1852Derivation(
        coin_type=Cryptocurrency.COIN_TYPE,
        account=0,
        role=ROLES.STAKING_KEY,
        address=0
    )
)

print(json.dumps(hdwallet.dump(exclude={"indexes"}), indent=4, ensure_ascii=False))
# print(json.dumps(hdwallet.dumps(exclude={"indexes"}), indent=4, ensure_ascii=False))
