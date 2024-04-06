#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.cryptocurrencies import Qtum as Cryptocurrency
from hdwallet.derivations import CustomDerivation
from hdwallet.const import PUBLIC_KEY_TYPES
from hdwallet.hds import BIP141HD

import json


hdwallet: HDWallet = HDWallet(
    cryptocurrency=Cryptocurrency,
    hd=BIP141HD,
    network=Cryptocurrency.NETWORKS.MAINNET,
    public_key_type=PUBLIC_KEY_TYPES.COMPRESSED
).from_xpublic_key(
    xpublic_key="xpub661MyMwAqRbcEYxcChjb28wcZSFGCJS5dz4MtqnkXvfcvG6RDHWwA8Yyj8huR1AnPaWwMjjwux3n6b5hNnTcgwYXSfCsi9RnQ6RvY3RZ8fm",
    strict=True
).from_derivation(
    derivation=CustomDerivation(
        path="m/0/0-2"  # Hardened "'" key is not allowed for xpublic key
    )
)

# print(json.dumps(hdwallet.dump(exclude={"indexes"}), indent=4, ensure_ascii=False))
print(json.dumps(hdwallet.dumps(exclude={"indexes"}), indent=4, ensure_ascii=False))
