#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.seeds import CardanoSeed
from hdwallet.cryptocurrencies import Cardano as Cryptocurrency
from hdwallet.hds import CardanoHD
from hdwallet.derivations import (
    CIP1852Derivation, ROLES
)

import json


hdwallet: HDWallet = HDWallet(
    cryptocurrency=Cryptocurrency,
    hd=CardanoHD,
    cardano_type=Cryptocurrency.TYPES.SHELLEY_ICARUS,
    address_type=Cryptocurrency.ADDRESS_TYPES.PAYMENT,
    staking_public_key="00f06973be3a2b8d74086283e18176b6b4b5bd28da78c264cd65ad146126f8240e",
    passphrase="meherett"
).from_seed(
    seed=CardanoSeed(
        seed="fca87b68fdffa968895901c894f678f6"
    )
).from_derivation(
    derivation=CIP1852Derivation(
        coin_type=Cryptocurrency.COIN_TYPE,
        account=0,
        role=ROLES.EXTERNAL_CHAIN,
        address=(6, 8)
    )
)

# print(json.dumps(hdwallet.dump(exclude={"indexes"}), indent=4, ensure_ascii=False))
print(json.dumps(hdwallet.dumps(exclude={"indexes"}), indent=4, ensure_ascii=False))
