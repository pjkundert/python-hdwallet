#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.cryptocurrencies.cardano import Cardano
from hdwallet.hds import CardanoHD
from hdwallet.entropies.bip39 import (
    BIP39Entropy, BIP39_ENTROPY_STRENGTHS
)
from hdwallet.mnemonics import BIP39_MNEMONIC_LANGUAGES
from hdwallet.derivations import BIP44Derivation

# Generate BIP39 entropy
entropy: str = BIP39Entropy.generate(
    strength=BIP39_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT
)
bip39_entropy: BIP39Entropy = BIP39Entropy(entropy=entropy)

# Initialize Byron-Ledger Cardano HDWallet
hdwallet: HDWallet = HDWallet(
    cryptocurrency=Cardano,
    hd=CardanoHD,
    language=BIP39_MNEMONIC_LANGUAGES.CHINESE_SIMPLIFIED,
    cardano_type=Cardano.TYPES.BYRON_LEDGER
)

# Update Byron-Ledger Cardano HDWallet
hdwallet.from_entropy(
    entropy=bip39_entropy
)

print("Cryptocurrency:", hdwallet.cryptocurrency())
print("Symbol:", hdwallet.symbol())
print("Type:", hdwallet.type())
print("Network:", hdwallet.network())
print("Entropy:", hdwallet.entropy())
print("Strength:", hdwallet.strength())
print("Mnemonic:", hdwallet.mnemonic())
print("Passphrase:", hdwallet.passphrase())
print("Language:", hdwallet.language())
print("Seed:", hdwallet.seed())
print("Root XPrivate Key:", hdwallet.root_xprivate_key())
print("Root XPublic Key:", hdwallet.root_xpublic_key())
print("Root Chain Code:", hdwallet.root_chain_code())
print("Root Private Key:", hdwallet.root_private_key())
print("Root Public Key:", hdwallet.root_public_key())

# Initialize BIP44 derivation
bip44_derivation: BIP44Derivation = BIP44Derivation(
    coin_type=Cardano.COIN_TYPE
)

# Update Byron-Ledger Cardano HDWallet derivation
hdwallet.from_derivation(
    derivation=bip44_derivation
)

print("XPrivate Key:", hdwallet.xprivate_key())
print("XPublic Key:", hdwallet.xpublic_key())
print("Private Key:", hdwallet.private_key())
print("Chain Code:", hdwallet.chain_code())
print("Public Key:", hdwallet.public_key())
print("Depth:", hdwallet.depth())
print("Path:", hdwallet.path())
print("Index:", hdwallet.index())
print("Indexes:", hdwallet.indexes())
print("Fingerprint:", hdwallet.fingerprint())
print("Parent Fingerprint:", hdwallet.parent_fingerprint())
print("Address:", hdwallet.address())
