#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.cryptocurrencies import Cardano as Cryptocurrency
from hdwallet.derivations import CustomDerivation
from hdwallet.hds import CardanoHD

import json


hdwallet: HDWallet = HDWallet(
    cryptocurrency=Cryptocurrency,
    hd=CardanoHD,
    cardano_type=Cryptocurrency.TYPES.BYRON_LEGACY
).from_xprivate_key(
    xprivate_key="xprv3QESAWYc9vDdZKQAwwfoRBaiWEiTMbMtfPuyREap66sm2yyrV5ipveHVwDccQejWaLqMqLxDYnuNssg4Mf19Mc7EtNuGqLxZPdkaCnR9YEqo3qJpsqBnRi3qkWdWmFZ6xbhNUk799jZqiBwW3ou7jcS",
    strict=True
).from_derivation(
    derivation=CustomDerivation(
        path="m/0'/0-2"
    )
)

# print(json.dumps(hdwallet.dump(exclude={"indexes"}), indent=4, ensure_ascii=False))
print(json.dumps(hdwallet.dumps(exclude={"indexes"}), indent=4, ensure_ascii=False))
