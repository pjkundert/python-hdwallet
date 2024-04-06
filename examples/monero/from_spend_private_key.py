#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.cryptocurrencies import Monero as Cryptocurrency
from hdwallet.derivations import MoneroDerivation
from hdwallet.hds import MoneroHD

import json


hdwallet: HDWallet = HDWallet(
    cryptocurrency=Cryptocurrency,
    hd=MoneroHD,
    network=Cryptocurrency.NETWORKS.MAINNET
).from_spend_private_key(
    spend_private_key="ee08ca4c8556cf0e8f32a1663f9b9a695be2ed4d561244f7127d3753e5f9c802"
).from_derivation(
    derivation=MoneroDerivation(
        minor=0, major=(0, 5)
    )
)

# print(json.dumps(hdwallet.dump(exclude={"indexes"}), indent=4, ensure_ascii=False))
print(json.dumps(hdwallet.dumps(exclude={"indexes"}), indent=4, ensure_ascii=False))
