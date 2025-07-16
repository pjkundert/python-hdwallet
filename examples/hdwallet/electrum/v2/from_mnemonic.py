#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.mnemonics import (
    ElectrumV2Mnemonic, ELECTRUM_V2_MNEMONIC_LANGUAGES, ELECTRUM_V2_MNEMONIC_TYPES, ELECTRUM_V2_MNEMONIC_WORDS
)
from hdwallet.derivations import ElectrumDerivation
from hdwallet.cryptocurrencies import Bitcoin
from hdwallet.consts import (
    MODES, PUBLIC_KEY_TYPES
)
from hdwallet.hds import ElectrumV2HD

import json


hdwallet: HDWallet = HDWallet(
    cryptocurrency=Bitcoin,
    hd=ElectrumV2HD,
    network=Bitcoin.NETWORKS.MAINNET,
    language=ELECTRUM_V2_MNEMONIC_LANGUAGES.SPANISH,
    mnemonic_type=ELECTRUM_V2_MNEMONIC_TYPES.SEGWIT,
    mode=MODES.SEGWIT,
    public_key_type=PUBLIC_KEY_TYPES.UNCOMPRESSED
).from_mnemonic(
    mnemonic=ElectrumV2Mnemonic(
        mnemonic=ElectrumV2Mnemonic.from_words(
            words=ELECTRUM_V2_MNEMONIC_WORDS.TWELVE,
            language=ELECTRUM_V2_MNEMONIC_LANGUAGES.SPANISH,
            mnemonic_type=ELECTRUM_V2_MNEMONIC_TYPES.SEGWIT,
        ),
        mnemonic_type=ELECTRUM_V2_MNEMONIC_TYPES.SEGWIT
    )
).from_derivation(
    derivation=ElectrumDerivation(
        change=0, address=0
    )
)

# print(json.dumps(hdwallet.dump(), indent=4, ensure_ascii=False))
print(json.dumps(hdwallet.dumps(), indent=4, ensure_ascii=False))
