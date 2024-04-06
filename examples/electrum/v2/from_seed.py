#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.seeds import ElectrumV2Seed
from hdwallet.derivations import ElectrumDerivation
from hdwallet.cryptocurrencies import Bitcoin
from hdwallet.const import (
    ELECTRUM_V2_MODES, PUBLIC_KEY_TYPES
)
from hdwallet.hds import ElectrumV2HD

import json


hdwallet: HDWallet = HDWallet(
    cryptocurrency=Bitcoin,
    hd=ElectrumV2HD,
    network=Bitcoin.NETWORKS.MAINNET,
    mode=ELECTRUM_V2_MODES.SEGWIT,
    public_key_type=PUBLIC_KEY_TYPES.UNCOMPRESSED
).from_seed(
    seed=ElectrumV2Seed(
        seed="4c423a08ccc9d0fe2fb6136ffdc5292a18c0a552e1246b572a5740c523052882880ca55faf84c996945c7f7145c84ddaedb671e8f23c9bff87617f67e9fb1319"
    )
).from_derivation(
    derivation=ElectrumDerivation(
        change=(0, 2), address=(1, 2)
    )
)

# print(json.dumps(hdwallet.dump(exclude={"indexes"}), indent=4, ensure_ascii=False))
print(json.dumps(hdwallet.dumps(exclude={"indexes"}), indent=4, ensure_ascii=False))
