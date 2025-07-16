#!/usr/bin/env python3

from hdwallet import HDWallet
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
).from_private_key(
    private_key="0fea3ff3b19b033672e8ac8a3b26fed252daf30762c8294e9dd62dc417d2108e"
).from_derivation(
    derivation=ElectrumDerivation(
        change=(0, 2), address=0
    )
)

# print(json.dumps(hdwallet.dump(exclude={"indexes"}), indent=4, ensure_ascii=False))
print(json.dumps(hdwallet.dumps(exclude={"indexes"}), indent=4, ensure_ascii=False))
