#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.cryptocurrencies import Cardano as Cryptocurrency
from hdwallet.hds import CardanoHD

import json


hdwallet: HDWallet = HDWallet(
    cryptocurrency=Cryptocurrency,
    hd=CardanoHD,
    cardano_type=Cryptocurrency.TYPES.SHELLEY_LEDGER,
    address_type=Cryptocurrency.ADDRESS_TYPES.STAKING
).from_public_key(
    public_key="00c76d02311731bdca7afe7907f2f3b53383d43f278d8c22abb73c17d417d37cf1"
)

print(json.dumps(hdwallet.dump(exclude={"indexes"}), indent=4, ensure_ascii=False))
