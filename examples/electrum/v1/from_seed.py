#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.seeds import ElectrumV1Seed
from hdwallet.derivations import ElectrumDerivation
from hdwallet.cryptocurrencies import Bitcoin
from hdwallet.const import PUBLIC_KEY_TYPES
from hdwallet.hds import ElectrumV1HD

import json


hdwallet: HDWallet = HDWallet(
    cryptocurrency=Bitcoin,
    hd=ElectrumV1HD,
    network=Bitcoin.NETWORKS.MAINNET,
    public_key_type=PUBLIC_KEY_TYPES.UNCOMPRESSED
).from_seed(
    seed=ElectrumV1Seed(
        seed="5e29d84b7fc49c29eb0c3888d6eed8239711ccf94109eb986ca6a9058e8ba274"
    )
).from_derivation(
    derivation=ElectrumDerivation(
        change=(0, 2), address=(1, 2)
    )
)

print(json.dumps(hdwallet.dump(exclude={"indexes"}), indent=4, ensure_ascii=False))
# print(json.dumps(hdwallet.dumps(exclude={"indexes"}), indent=4, ensure_ascii=False))
