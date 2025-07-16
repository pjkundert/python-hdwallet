#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.mnemonics import (
    ElectrumV1Mnemonic, ELECTRUM_V1_MNEMONIC_LANGUAGES, ELECTRUM_V1_MNEMONIC_WORDS
)
from hdwallet.derivations import ElectrumDerivation
from hdwallet.cryptocurrencies import Bitcoin
from hdwallet.consts import PUBLIC_KEY_TYPES
from hdwallet.hds import ElectrumV1HD

import json


hdwallet: HDWallet = HDWallet(
    cryptocurrency=Bitcoin,
    hd=ElectrumV1HD,
    network=Bitcoin.NETWORKS.MAINNET,
    public_key_type=PUBLIC_KEY_TYPES.UNCOMPRESSED
).from_mnemonic(
    mnemonic=ElectrumV1Mnemonic(
        mnemonic=ElectrumV1Mnemonic.from_words(
            words=ELECTRUM_V1_MNEMONIC_WORDS.TWELVE,
            language=ELECTRUM_V1_MNEMONIC_LANGUAGES.ENGLISH
        )
    )
).from_derivation(
    derivation=ElectrumDerivation(
        change=0, address=1
    )
)

print(json.dumps(hdwallet.dump(), indent=4, ensure_ascii=False))
# print(json.dumps(hdwallet.dumps(), indent=4, ensure_ascii=False))
