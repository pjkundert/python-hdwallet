#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.seeds import AlgorandSeed
from hdwallet.cryptocurrencies import Algorand as Cryptocurrency
from hdwallet.consts import PUBLIC_KEY_TYPES
from hdwallet.derivations import (
    BIP44Derivation, CHANGES
)
from hdwallet.hds import BIP32HD

import json


hdwallet: HDWallet = HDWallet(
    cryptocurrency=Cryptocurrency,
    hd=BIP32HD,
    network=Cryptocurrency.NETWORKS.MAINNET,
    public_key_type=PUBLIC_KEY_TYPES.COMPRESSED
).from_seed(
    seed=AlgorandSeed(
        seed="680dca0430704e98224ea64e48964f647d6a428116e629f83c34fe37f799712a"
    )
).from_derivation(
    derivation=BIP44Derivation(
        coin_type=Cryptocurrency.COIN_TYPE,
        account=0,
        change=CHANGES.EXTERNAL_CHAIN,
        address=0
    )
)

print(json.dumps(hdwallet.dump(exclude={"indexes"}), indent=4, ensure_ascii=False))
# print(json.dumps(hdwallet.dumps(exclude={"indexes"}), indent=4, ensure_ascii=False))
