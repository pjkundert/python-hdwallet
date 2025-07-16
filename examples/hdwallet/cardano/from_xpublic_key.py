#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.cryptocurrencies import Cardano as Cryptocurrency
from hdwallet.derivations import CustomDerivation
from hdwallet.hds import CardanoHD

import json


hdwallet: HDWallet = HDWallet(
    cryptocurrency=Cryptocurrency,
    hd=CardanoHD,
    cardano_type=Cryptocurrency.TYPES.BYRON_LEDGER  # Not supported for byton-legacy
).from_xpublic_key(
    xpublic_key="xpub661MyMwAqRbcEiUJew81QNEAr6jYLVSksDzdQUtWbSWLRdA8ouX1bqK1WxS4qdF4gu8VwSxDVX7n216daK1735md81Z1L7uFUAAT4eSN1xr",
    strict=True
).from_derivation(
    derivation=CustomDerivation(
        path="m/0/0-2"  # Hardened "'" key is not allowed for xpublic key
    )
)

# print(json.dumps(hdwallet.dump(exclude={"indexes"}), indent=4, ensure_ascii=False))
print(json.dumps(hdwallet.dumps(exclude={"indexes"}), indent=4, ensure_ascii=False))
