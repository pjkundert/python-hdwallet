#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from ..ecc import SLIP10Secp256k1ECC
from ..const import (
    Info, WitnessVersions, Entropies, Mnemonics, Seeds, HDs, Addresses, Networks, XPrivateKeyVersions, XPublicKeyVersions
)
from .icryptocurrency import (
    ICryptocurrency, INetwork
)


class Mainnet(INetwork):

    PUBLIC_KEY_ADDRESS_PREFIX = 0x00
    SCRIPT_ADDRESS_PREFIX = 0x05
    HRP = "bc"
    WITNESS_VERSIONS = WitnessVersions({
        "P2TR": 0x01,
        "P2WPKH": 0x00,
        "P2WSH": 0x00
    })
    XPRIVATE_KEY_VERSIONS = XPrivateKeyVersions({
        "P2PKH": 0x0488ade4,
        "P2SH": 0x0488ade4,
        "P2WPKH": 0x04b2430c,
        "P2WPKH_IN_P2SH": 0x049d7878,
        "P2WSH": 0x02aa7a99,
        "P2WSH_IN_P2SH": 0x0295b005
    })
    XPUBLIC_KEY_VERSIONS = XPublicKeyVersions({
        "P2PKH": 0x0488b21e,
        "P2SH": 0x0488b21e,
        "P2WPKH": 0x04b24746,
        "P2WPKH_IN_P2SH": 0x049d7cb2,
        "P2WSH": 0x02aa7ed3,
        "P2WSH_IN_P2SH": 0x0295b43f
    })
    MESSAGE_PREFIX = "\x18Bitcoin Signed Message:\n"
    WIF_PREFIX = 0x80


class Testnet(INetwork):

    PUBLIC_KEY_ADDRESS_PREFIX = 0x6f
    SCRIPT_ADDRESS_PREFIX = 0xc4
    HRP = "tb"
    WITNESS_VERSIONS = WitnessVersions({
        "P2TR": 0x01,
        "P2WPKH": 0x00,
        "P2WSH": 0x00
    })
    XPRIVATE_KEY_VERSIONS = XPrivateKeyVersions({
        "P2PKH": 0x04358394,
        "P2SH": 0x04358394,
        "P2WPKH": 0x045f18bc,
        "P2WPKH_IN_P2SH": 0x044a4e28,
        "P2WSH": 0x02575048,
        "P2WSH_IN_P2SH": 0x024285b5
    })
    XPUBLIC_KEY_VERSIONS = XPublicKeyVersions({
        "P2PKH": 0x043587cf,
        "P2SH": 0x043587cf,
        "P2WPKH": 0x045f1cf6,
        "P2WPKH_IN_P2SH": 0x044a5262,
        "P2WSH": 0x02575483,
        "P2WSH_IN_P2SH": 0x024289ef
    })
    MESSAGE_PREFIX = "\x18Bitcoin Signed Message:\n"
    WIF_PREFIX = 0xef


class Bitcoin(ICryptocurrency):

    NAME = "Bitcoin"
    SYMBOL = "BTC"
    INFO = Info({
        "SOURCE_CODE": "https://github.com/bitcoin/bitcoin",
        "WHITEPAPER": "https://bitcoin.org/bitcoin.pdf",
        "WEBSITES": [
            "https://bitcoin.org"
        ]
    })
    ECC = SLIP10Secp256k1ECC
    COIN_TYPE = 0
    NETWORKS = Networks({
        "MAINNET": Mainnet, "TESTNET": Testnet
    })
    DEFAULT_NETWORK = NETWORKS.MAINNET
    ENTROPIES = Entropies((
        "BIP39", {"ELECTRUM_V1": "Electrum-V1"}, {"ELECTRUM_V2": "Electrum-V2"}
    ))
    MNEMONICS = Mnemonics((
        "BIP39", {"ELECTRUM_V1": "Electrum-V1"}, {"ELECTRUM_V2": "Electrum-V2"}
    ))
    SEEDS = Seeds((
        "BIP39", {"ELECTRUM_V1": "Electrum-V1"}, {"ELECTRUM_V2": "Electrum-V2"}
    ))
    HDS = HDs((
        "BIP32", "BIP44", "BIP49", "BIP84", "BIP86", "BIP141", {"ELECTRUM_V1": "Electrum-V1"}, {"ELECTRUM_V2": "Electrum-V2"}
    ))
    DEFAULT_HD = HDS.BIP44
    ADDRESSES = Addresses((
        "P2PKH", "P2SH", "P2TR", "P2WPKH", {"P2WPKH_IN_P2SH": "P2WPKH-In-P2SH"}, "P2WSH", {"P2WSH_IN_P2SH": "P2WSH-In-P2SH"}
    ))
    DEFAULT_ADDRESS = ADDRESSES.P2PKH
