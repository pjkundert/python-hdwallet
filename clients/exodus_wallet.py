#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.eccs import (
    SLIP10Secp256k1ECC, SLIP10Ed25519ECC, SLIP10Nist256p1ECC
)
from hdwallet.seeds.bip39 import BIP39Seed
from hdwallet.cryptocurrencies import (
    Algorand, Solana, Stellar, Neo
)
from hdwallet.hds import BIP44HD

# Get BIP39 mnemonic
mnemonic: str = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"

# Get BIP39 seed
seed: str = BIP39Seed.from_mnemonic(
    mnemonic=mnemonic, passphrase=None
)


for Cryptocurrency, ECC in [
    (Algorand, SLIP10Ed25519ECC),
    (Solana, SLIP10Ed25519ECC),
    (Stellar, SLIP10Ed25519ECC),
    (Neo, SLIP10Nist256p1ECC)
]:
    # Initialize SLIP10-Secp256k1 BIP44 HD and update root keys from seed
    bip44_hd: BIP44HD = BIP44HD(
        ecc=SLIP10Secp256k1ECC, coin_type=Cryptocurrency.COIN_TYPE
    ).from_seed(seed=BIP39Seed(seed=seed))

    # Initialize Cryptocurrency HDWallet
    hdwallet: HDWallet = HDWallet(
        ecc=ECC,
        cryptocurrency=Cryptocurrency,
        hd=BIP44HD,
        network=Cryptocurrency.NETWORKS.MAINNET,
        passphrase=None
    ).from_private_key(  # Get Cryptocurrency HDWallet from private key
        private_key=bip44_hd.private_key()  # Use the last private key as a master key
    )

    # Same address of Exodus
    print(f"Address for {Cryptocurrency.NAME}: {hdwallet.address()}")

