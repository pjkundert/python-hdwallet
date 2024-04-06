#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.entropies import (
    BIP39Entropy, BIP39_ENTROPY_STRENGTHS
)
from hdwallet.mnemonics import BIP39_MNEMONIC_LANGUAGES
from hdwallet.cryptocurrencies import Cardano as Cryptocurrency
from hdwallet.hds import CardanoHD
from hdwallet.derivations import (
    BIP44Derivation, CHANGES
)

import json


hdwallet: HDWallet = HDWallet(
    cryptocurrency=Cryptocurrency,
    hd=CardanoHD,
    language=BIP39_MNEMONIC_LANGUAGES.CZECH,
    cardano_type=Cryptocurrency.TYPES.BYRON_ICARUS,
    passphrase="meherett"
).from_entropy(
    entropy=BIP39Entropy(
        entropy=BIP39Entropy.generate(
            strength=BIP39_ENTROPY_STRENGTHS.TWO_HUNDRED_TWENTY_FOUR
        )
    )
).from_derivation(
    derivation=BIP44Derivation(
        coin_type=Cryptocurrency.COIN_TYPE,
        account=(0, 2),
        change=CHANGES.EXTERNAL_CHAIN,
        address=452
    )
)

# print(json.dumps(hdwallet.dump(exclude={"indexes"}), indent=4, ensure_ascii=False))
print(json.dumps(hdwallet.dumps(exclude={"indexes"}), indent=4, ensure_ascii=False))
