#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from hdwallet import HDWallet
from hdwallet.cryptocurrencies import CRYPTOCURRENCIES
from hdwallet.derivations import DERIVATIONS
from hdwallet.hds import HDS
from hdwallet.seeds import BIP39Seed


def test_bip141_from_seed_compressed(data):

    cryptocurrency = CRYPTOCURRENCIES.cryptocurrency(
        data["hdwallet"]["BIP141"]["compressed"]["cryptocurrency"]
    )
    hdwallet: HDWallet = HDWallet(
        cryptocurrency=cryptocurrency,
        hd=HDS.hd(
            data["hdwallet"]["BIP141"]["compressed"]["hd"]
        ),
        network=data["hdwallet"]["BIP141"]["compressed"]["network"],
        language=data["hdwallet"]["BIP141"]["compressed"]["language"].lower(),
        public_key_type=data["hdwallet"]["BIP141"]["compressed"]["public_key_type"]
    ).from_seed(
        seed=BIP39Seed(
            seed=data["hdwallet"]["BIP141"]["compressed"]["seed"]
        )
    ).from_derivation(
        derivation=DERIVATIONS.derivation(data["hdwallet"]["BIP141"]["derivation"]["name"])(
            **data["hdwallet"]["BIP141"]["derivation"]["args"]
        )
    )

    dump = data["hdwallet"]["BIP141"]["compressed"].copy()
    dump.update({
        "entropy": None,
        "strength": None,
        "mnemonic": None,
        "passphrase": None,
        "language": None
    })
    assert hdwallet.dumps() == dump

    del dump["derivations"]
    dump["derivation"] = data["hdwallet"]["BIP141"]["compressed"]["derivations"][-1].copy()

    assert hdwallet.dump() == dump

    assert hdwallet.cryptocurrency() == dump["cryptocurrency"]
    assert hdwallet.symbol() == dump["symbol"]
    assert hdwallet.network() == dump["network"]
    assert hdwallet.coin_type() == dump["coin_type"]
    assert hdwallet.entropy() == dump["entropy"]
    assert hdwallet.strength() == dump["strength"]
    assert hdwallet.mnemonic() == dump["mnemonic"]
    assert hdwallet.language() == dump["language"]
    assert hdwallet.seed() ==  dump["seed"]
    assert hdwallet.ecc() == dump["ecc"]
    assert hdwallet.hd() == dump["hd"]
    assert hdwallet.root_xprivate_key() == dump["root_xprivate_key"]
    assert hdwallet.root_xpublic_key() == dump["root_xpublic_key"]
    assert hdwallet.root_private_key() == dump["root_private_key"]
    assert hdwallet.root_wif() == dump["root_wif"]
    assert hdwallet.root_chain_code() == dump["root_chain_code"]
    assert hdwallet.root_public_key() == dump["root_public_key"]
    assert hdwallet.strict() == dump["strict"]
    assert hdwallet.public_key_type() == dump["public_key_type"]
    assert hdwallet.wif_type() == dump["wif_type"]

    assert hdwallet.xprivate_key() == dump["derivation"]["xprivate_key"]
    assert hdwallet.xpublic_key() == dump["derivation"]["xpublic_key"]
    assert hdwallet.private_key() == dump["derivation"]["private_key"]
    assert hdwallet.wif() == dump["derivation"]["wif"]
    assert hdwallet.chain_code() == dump["derivation"]["chain_code"]
    assert hdwallet.public_key() == dump["derivation"]["public_key"]
    assert hdwallet.uncompressed() == dump["derivation"]["uncompressed"]
    assert hdwallet.compressed() == dump["derivation"]["compressed"]
    assert hdwallet.hash() == dump["derivation"]["hash"]
    assert hdwallet.fingerprint() == dump["derivation"]["fingerprint"]
    assert hdwallet.parent_fingerprint() == dump["derivation"]["parent_fingerprint"]

    assert hdwallet.address(
        address=cryptocurrency.ADDRESSES.P2WPKH,
        hrp=cryptocurrency.NETWORKS.MAINNET.HRP,
        witness_version=cryptocurrency.NETWORKS.MAINNET.WITNESS_VERSIONS.P2WPKH
    ) == dump["derivation"]["addresses"]["p2wpkh"]
    assert hdwallet.address(
        address=cryptocurrency.ADDRESSES.P2WPKH_IN_P2SH,
        script_address_prefix=cryptocurrency.NETWORKS.MAINNET.SCRIPT_ADDRESS_PREFIX
    ) == dump["derivation"]["addresses"]["p2wpkh_in_p2sh"]
    assert hdwallet.address(
        address=cryptocurrency.ADDRESSES.P2WSH,
        hrp=cryptocurrency.NETWORKS.MAINNET.HRP,
        witness_version=cryptocurrency.NETWORKS.MAINNET.WITNESS_VERSIONS.P2WSH
    ) == dump["derivation"]["addresses"]["p2wsh"]
    assert hdwallet.address(
        address=cryptocurrency.ADDRESSES.P2WSH_IN_P2SH,
        script_address_prefix=cryptocurrency.NETWORKS.MAINNET.SCRIPT_ADDRESS_PREFIX
    ) == dump["derivation"]["addresses"]["p2wsh_in_p2sh"]


def test_bip141_from_seed_uncompressed(data):

    cryptocurrency = CRYPTOCURRENCIES.cryptocurrency(
        data["hdwallet"]["BIP141"]["uncompressed"]["cryptocurrency"]
    )
    hdwallet: HDWallet = HDWallet(
        cryptocurrency=cryptocurrency,
        hd=HDS.hd(
            data["hdwallet"]["BIP141"]["uncompressed"]["hd"]
        ),
        network=data["hdwallet"]["BIP141"]["uncompressed"]["network"],
        language=data["hdwallet"]["BIP141"]["uncompressed"]["language"].lower(),
        public_key_type=data["hdwallet"]["BIP141"]["uncompressed"]["public_key_type"]
    ).from_seed(
        seed=BIP39Seed(
            seed=data["hdwallet"]["BIP141"]["uncompressed"]["seed"]
        )
    ).from_derivation(
        derivation=DERIVATIONS.derivation(data["hdwallet"]["BIP141"]["derivation"]["name"])(
            **data["hdwallet"]["BIP141"]["derivation"]["args"]
        )
    )

    dump = data["hdwallet"]["BIP141"]["uncompressed"].copy()
    dump.update({
        "entropy": None,
        "strength": None,
        "mnemonic": None,
        "passphrase": None,
        "language": None
    })
    assert hdwallet.dumps() == dump

    del dump["derivations"]
    dump["derivation"] = data["hdwallet"]["BIP141"]["uncompressed"]["derivations"][-1].copy()

    assert hdwallet.dump() == dump

    assert hdwallet.cryptocurrency() == dump["cryptocurrency"]
    assert hdwallet.symbol() == dump["symbol"]
    assert hdwallet.network() == dump["network"]
    assert hdwallet.coin_type() == dump["coin_type"]
    assert hdwallet.entropy() == dump["entropy"]
    assert hdwallet.strength() == dump["strength"]
    assert hdwallet.mnemonic() == dump["mnemonic"]
    assert hdwallet.language() == dump["language"]
    assert hdwallet.seed() ==  dump["seed"]
    assert hdwallet.ecc() == dump["ecc"]
    assert hdwallet.hd() == dump["hd"]
    assert hdwallet.root_xprivate_key() == dump["root_xprivate_key"]
    assert hdwallet.root_xpublic_key() == dump["root_xpublic_key"]
    assert hdwallet.root_private_key() == dump["root_private_key"]
    assert hdwallet.root_wif() == dump["root_wif"]
    assert hdwallet.root_chain_code() == dump["root_chain_code"]
    assert hdwallet.root_public_key() == dump["root_public_key"]
    assert hdwallet.strict() == dump["strict"]
    assert hdwallet.public_key_type() == dump["public_key_type"]
    assert hdwallet.wif_type() == dump["wif_type"]

    assert hdwallet.xprivate_key() == dump["derivation"]["xprivate_key"]
    assert hdwallet.xpublic_key() == dump["derivation"]["xpublic_key"]
    assert hdwallet.private_key() == dump["derivation"]["private_key"]
    assert hdwallet.wif() == dump["derivation"]["wif"]
    assert hdwallet.chain_code() == dump["derivation"]["chain_code"]
    assert hdwallet.public_key() == dump["derivation"]["public_key"]
    assert hdwallet.uncompressed() == dump["derivation"]["uncompressed"]
    assert hdwallet.compressed() == dump["derivation"]["compressed"]
    assert hdwallet.hash() == dump["derivation"]["hash"]
    assert hdwallet.fingerprint() == dump["derivation"]["fingerprint"]
    assert hdwallet.parent_fingerprint() == dump["derivation"]["parent_fingerprint"]

    assert hdwallet.address(
        address=cryptocurrency.ADDRESSES.P2WPKH,
        hrp=cryptocurrency.NETWORKS.MAINNET.HRP,
        witness_version=cryptocurrency.NETWORKS.MAINNET.WITNESS_VERSIONS.P2WPKH
    ) == dump["derivation"]["addresses"]["p2wpkh"]
    assert hdwallet.address(
        address=cryptocurrency.ADDRESSES.P2WPKH_IN_P2SH,
        script_address_prefix=cryptocurrency.NETWORKS.MAINNET.SCRIPT_ADDRESS_PREFIX
    ) == dump["derivation"]["addresses"]["p2wpkh_in_p2sh"]
    assert hdwallet.address(
        address=cryptocurrency.ADDRESSES.P2WSH,
        hrp=cryptocurrency.NETWORKS.MAINNET.HRP,
        witness_version=cryptocurrency.NETWORKS.MAINNET.WITNESS_VERSIONS.P2WSH
    ) == dump["derivation"]["addresses"]["p2wsh"]
    assert hdwallet.address(
        address=cryptocurrency.ADDRESSES.P2WSH_IN_P2SH,
        script_address_prefix=cryptocurrency.NETWORKS.MAINNET.SCRIPT_ADDRESS_PREFIX
    ) == dump["derivation"]["addresses"]["p2wsh_in_p2sh"]
