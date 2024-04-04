#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.cryptocurrencies.cardano import Cardano
from hdwallet.hds import CardanoHD
from hdwallet.entropies.bip39 import (
    BIP39Entropy, BIP39_ENTROPY_STRENGTHS
)
from hdwallet.mnemonics import BIP39_MNEMONIC_LANGUAGES
from hdwallet.derivations import (
    CIP1852Derivation, ROLES
)

# Generate BIP39 entropy
entropy: str = BIP39Entropy.generate(
    strength=BIP39_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT
)
bip39_entropy: BIP39Entropy = BIP39Entropy(entropy=entropy)

# Initialize Shelley-Ledger Cardano HDWallet
hdwallet: HDWallet = HDWallet(
    cryptocurrency=Cardano,
    hd=CardanoHD,
    network=Cardano.NETWORKS.MAINNET,
    language=BIP39_MNEMONIC_LANGUAGES.PORTUGUESE,
    cardano_type=Cardano.TYPES.SHELLEY_LEDGER
)

# Update Shelley-Ledger Cardano HDWallet
hdwallet.from_entropy(
    entropy=bip39_entropy
)

print("Cryptocurrency:", hdwallet.cryptocurrency())
print("Symbol:", hdwallet.symbol())
print("Network:", hdwallet.network())
print("Entropy:", hdwallet.entropy())
print("Strength:", hdwallet.strength())
print("Mnemonic:", hdwallet.mnemonic())
print("Passphrase:", hdwallet.passphrase())
print("Language:", hdwallet.language())
print("Seed:", hdwallet.seed())
print("Cardano Type:", hdwallet.cardano_type())
print("Root XPrivate Key:", hdwallet.root_xprivate_key())
print("Root XPublic Key:", hdwallet.root_xpublic_key())
print("Root Chain Code:", hdwallet.root_chain_code())
print("Root Private Key:", hdwallet.root_private_key())
print("Root Public Key:", hdwallet.root_public_key())

# Initialize CIP1852 derivation
cip1852_derivation: CIP1852Derivation = CIP1852Derivation(
    role=ROLES.STAKING_KEY  # https://cips.cardano.org/cips/cip11
)

# Update Shelley-Ledger Cardano HDWallet derivation
hdwallet.from_derivation(
    derivation=cip1852_derivation
)

print("Staking XPrivate Key:", hdwallet.xprivate_key())
print("Staking XPublic Key:", hdwallet.xpublic_key())
print("Staking Private Key:", hdwallet.private_key())
print("Staking Chain Code:", hdwallet.chain_code())
staking_public_key: str = hdwallet.public_key()
print("Staking Public Key:", staking_public_key)
print("Staking Depth:", hdwallet.depth())
print("Staking Path:", hdwallet.path())
print("Staking Index:", hdwallet.index())
print("Staking Indexes:", hdwallet.indexes())
print("Staking Fingerprint:", hdwallet.fingerprint())
print("Staking Parent Fingerprint:", hdwallet.parent_fingerprint())
print("Staking Address:", hdwallet.address(
    address_type=Cardano.ADDRESS_TYPES.STAKING
))

# Change CIP1852 derivation
cip1852_derivation.from_role(
    role=ROLES.EXTERNAL_CHAIN
)

# Update Shelley-Ledger Cardano HDWallet derivation
hdwallet.update_derivation(
    derivation=cip1852_derivation
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
print("Address:", hdwallet.address(
    address_type=Cardano.ADDRESS_TYPES.PAYMENT, staking_public_key=staking_public_key
))
