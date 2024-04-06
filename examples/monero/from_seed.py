#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.seeds import MoneroSeed
from hdwallet.cryptocurrencies import Monero as Cryptocurrency
from hdwallet.derivations import MoneroDerivation
from hdwallet.hds import MoneroHD

import json


hdwallet: HDWallet = HDWallet(
    cryptocurrency=Cryptocurrency,
    hd=MoneroHD,
    network=Cryptocurrency.NETWORKS.MAINNET,
    payment_id="ad17dc6e6793d178"
).from_seed(
    seed=MoneroSeed(
        seed="747bf6f08db7260c80a21bf6faae491c"
    )
).from_derivation(
    derivation=MoneroDerivation(
        minor=0, major=5
    )
)

print(json.dumps(hdwallet.dump(exclude={"indexes"}), indent=4, ensure_ascii=False))
# print(json.dumps(hdwallet.dumps(exclude={"indexes"}), indent=4, ensure_ascii=False))
