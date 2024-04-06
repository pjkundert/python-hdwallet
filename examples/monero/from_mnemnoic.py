#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.mnemonics import (
    MoneroMnemonic, MONERO_MNEMONIC_LANGUAGES, MONERO_MNEMONIC_WORDS
)
from hdwallet.cryptocurrencies import Monero as Cryptocurrency
from hdwallet.derivations import MoneroDerivation
from hdwallet.hds import MoneroHD

import json


hdwallet: HDWallet = HDWallet(
    cryptocurrency=Cryptocurrency,
    hd=MoneroHD,
    network=Cryptocurrency.NETWORKS.MAINNET,
    payment_id="ad17dc6e6793d178"
).from_mnemonic(
    mnemonic=MoneroMnemonic(
        mnemonic=MoneroMnemonic.from_words(
            words=MONERO_MNEMONIC_WORDS.TWELVE,
            language=MONERO_MNEMONIC_LANGUAGES.DUTCH
        )
    )
).from_derivation(
    derivation=MoneroDerivation(
        minor=0, major=5
    )
)

print(json.dumps(hdwallet.dump(), indent=4, ensure_ascii=False))
# print(json.dumps(hdwallet.dumps(), indent=4, ensure_ascii=False))
