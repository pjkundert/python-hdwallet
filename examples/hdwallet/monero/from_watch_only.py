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
).from_watch_only(
    view_private_key="c6542d68c6a33d68d80f2ae4c7668f943772152c32a564512b16bc5e10ca460c",
    spend_public_key="f40f86a5c4742a17561fb67a8516bcdbca82ce7cab20f575a677e88444b3f517"
).from_derivation(
    derivation=MoneroDerivation(
        minor=0, major=5
    )
)

print(json.dumps(hdwallet.dump(exclude={"indexes"}), indent=4, ensure_ascii=False))
# print(json.dumps(hdwallet.dumps(exclude={"indexes"}), indent=4, ensure_ascii=False))
