#!/usr/bin/env python3

from hdwallet.entropies import (
    ElectrumV1Entropy, ELECTRUM_V1_ENTROPY_STRENGTHS
)
from hdwallet.mnemonics import ELECTRUM_V1_MNEMONIC_LANGUAGES
from hdwallet.derivations import ElectrumDerivation
from hdwallet.cryptocurrencies import Bitcoin
from hdwallet.const import PUBLIC_KEY_TYPES
from hdwallet.hds import ElectrumV1HD
from hdwallet import HDWallet

import json


hdwallet: HDWallet = HDWallet(
    cryptocurrency=Bitcoin,
    hd=ElectrumV1HD,
    network=Bitcoin.NETWORKS.MAINNET,
    language=ELECTRUM_V1_MNEMONIC_LANGUAGES.ENGLISH,
    public_key_type=PUBLIC_KEY_TYPES.UNCOMPRESSED
).from_entropy(
    entropy=ElectrumV1Entropy(
        entropy=ElectrumV1Entropy.generate(
            strength=ELECTRUM_V1_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT
        )
    )
).from_derivation(
    derivation=ElectrumDerivation(
        change=0, address=5
    )
)

print(json.dumps(hdwallet.dump(), indent=4, ensure_ascii=False))
