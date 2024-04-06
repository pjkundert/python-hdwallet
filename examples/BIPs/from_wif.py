#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.cryptocurrencies import Bitcoin as Cryptocurrency
from hdwallet.const import PUBLIC_KEY_TYPES
from hdwallet.hds import BIP86HD

import json


hdwallet: HDWallet = HDWallet(
    cryptocurrency=Cryptocurrency,
    hd=BIP86HD,
    network=Cryptocurrency.NETWORKS.MAINNET,
    public_key_type=PUBLIC_KEY_TYPES.UNCOMPRESSED
).from_wif(
    wif="KwkeWuENpJSiPpUtrqFCXYbcU8zhJFuCg8ydwVg6ewUn3Wc1Jhek"
)

print(json.dumps(hdwallet.dump(exclude={"indexes"}), indent=4, ensure_ascii=False))
