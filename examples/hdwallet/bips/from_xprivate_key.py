#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.cryptocurrencies import Bitcoin as Cryptocurrency
from hdwallet.derivations import CustomDerivation
from hdwallet.consts import (
    PUBLIC_KEY_TYPES, SEMANTICS
)
from hdwallet.hds import BIP141HD

import json


hdwallet: HDWallet = HDWallet(
    cryptocurrency=Cryptocurrency,
    hd=BIP141HD,
    network=Cryptocurrency.NETWORKS.MAINNET,
    public_key_type=PUBLIC_KEY_TYPES.COMPRESSED,
    semantic=SEMANTICS.P2WPKH_IN_P2SH
).from_xprivate_key(
    xprivate_key="xprv9s21ZrQH143K24t96gCaezzt1QQmnqiEGm8m6TP8yb8e3TmGfkCgcLEVsskufMW9R4KH27pD1kyyEfJkYz1eiPwjhFzB4gtabH3PzMSmXSM",
    strict=True
).from_derivation(
    derivation=CustomDerivation(
        path="m/0'/0-2"
    )
)

# print(json.dumps(hdwallet.dump(exclude={"indexes"}), indent=4, ensure_ascii=False))
print(json.dumps(hdwallet.dumps(exclude={"indexes"}), indent=4, ensure_ascii=False))
