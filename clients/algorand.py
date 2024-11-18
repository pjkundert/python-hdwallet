#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.mnemonics.algorand import (
    AlgorandMnemonic, ALGORAND_MNEMONIC_LANGUAGES, ALGORAND_MNEMONIC_WORDS
)
from hdwallet.seeds.algorand import AlgorandSeed
from hdwallet.cryptocurrencies import Algorand as Cryptocurrency
from hdwallet.hds import BIP44HD

import json

# Get Algorand mnemonic
mnemonic: str = AlgorandMnemonic.from_words(
    words=ALGORAND_MNEMONIC_WORDS.TWENTY_FIVE, language=ALGORAND_MNEMONIC_LANGUAGES.ENGLISH
)
algorand_mnemonic: AlgorandMnemonic = AlgorandMnemonic(mnemonic=mnemonic)
print("Algorand Mnemonic:", algorand_mnemonic.mnemonic())
print("Algorand Language:", algorand_mnemonic.language())
print("Algorand Words:", algorand_mnemonic.words())

# Get Algorand seed
seed: str = AlgorandSeed.from_mnemonic(
    mnemonic=algorand_mnemonic
)

# Initialize Algorand HDWallet
hdwallet: HDWallet = HDWallet(
    cryptocurrency=Cryptocurrency,
    hd=BIP44HD,
    network=Cryptocurrency.NETWORKS.MAINNET,
    passphrase=None
).from_private_key(   # Get Algorand HDWallet from private key
    private_key=seed  # Use seed directly as private key
)

print(json.dumps(hdwallet.dump(exclude={
    "root", "indexes", "xprivate_key", "xpublic_key"
}), indent=4, ensure_ascii=False))
