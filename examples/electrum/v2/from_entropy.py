#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.entropies import (
    ElectrumV2Entropy, ELECTRUM_V2_ENTROPY_STRENGTHS
)
from hdwallet.mnemonics import (
    ELECTRUM_V2_MNEMONIC_LANGUAGES, ELECTRUM_V2_MNEMONIC_TYPES
)
from hdwallet.derivations import ElectrumDerivation
from hdwallet.cryptocurrencies import Bitcoin
from hdwallet.const import (
    MODES, PUBLIC_KEY_TYPES
)
from hdwallet.hds import ElectrumV2HD

import json


hdwallet: HDWallet = HDWallet(
    cryptocurrency=Bitcoin,
    hd=ElectrumV2HD,
    network=Bitcoin.NETWORKS.MAINNET,
    language=ELECTRUM_V2_MNEMONIC_LANGUAGES.PORTUGUESE,
    mnemonic_type=ELECTRUM_V2_MNEMONIC_TYPES.SEGWIT,
    mode=MODES.SEGWIT,
    public_key_type=PUBLIC_KEY_TYPES.UNCOMPRESSED
).from_entropy(
    entropy=ElectrumV2Entropy(
        entropy=ElectrumV2Entropy.generate(
            strength=ELECTRUM_V2_ENTROPY_STRENGTHS.ONE_HUNDRED_THIRTY_TWO
        )
    )
).from_derivation(
    derivation=ElectrumDerivation(
        change=(1, 2), address=(1, 2)
    )
)

# print(json.dumps(hdwallet.dump(), indent=4, ensure_ascii=False))
print(json.dumps(hdwallet.dumps(), indent=4, ensure_ascii=False))
