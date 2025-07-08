#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Optional, Union, Type
)

from ..ecc import IEllipticCurveCryptography
from ..derivations.bip44 import BIP44Derivation
from ..const import (
    Info, WitnessVersions, Entropies, Mnemonics, Seeds, HDs, Addresses, AddressTypes, AddressPrefixes, Networks, Params, XPrivateKeyVersions, XPublicKeyVersions
)
from ..exceptions import NetworkError


class INetwork:

    NAME: str
    # Bitcoin
    PUBLIC_KEY_ADDRESS_PREFIX: Optional[int] = None
    SCRIPT_ADDRESS_PREFIX: Optional[int] = None
    HRP: Optional[str] = None
    WITNESS_VERSIONS: Optional[WitnessVersions] = None
    XPRIVATE_KEY_VERSIONS: Optional[XPrivateKeyVersions] = None
    XPUBLIC_KEY_VERSIONS: Optional[XPublicKeyVersions] = None
    MESSAGE_PREFIX: Optional[str] = None
    WIF_PREFIX: Optional[int] = None
    # Bitcoin-Cash | Bitcoin-Cash-SLP | eCash
    LEGACY_PUBLIC_KEY_ADDRESS_PREFIX: Optional[int] = None
    STD_PUBLIC_KEY_ADDRESS_PREFIX: Optional[int] = None
    LEGACY_SCRIPT_ADDRESS_PREFIX: Optional[int] = None
    STD_SCRIPT_ADDRESS_PREFIX: Optional[int] = None
    # Monero
    STANDARD: Optional[int] = None
    INTEGRATED: Optional[int] = None
    SUB_ADDRESS: Optional[int] = None
    # Cardano
    TYPE: Optional[int] = None
    PAYMENT_ADDRESS_HRP: Optional[str] = None
    REWARD_ADDRESS_HRP: Optional[str] = None


class ICryptocurrency:

    NAME: str
    SYMBOL: str
    INFO: Info
    ECC: Type[IEllipticCurveCryptography]
    COIN_TYPE: int
    SUPPORT_BIP38: bool = False
    NETWORKS: Networks
    DEFAULT_NETWORK: INetwork
    ENTROPIES: Entropies
    MNEMONICS: Mnemonics
    SEEDS: Seeds
    HDS: HDs
    DEFAULT_HD: str
    DEFAULT_PATH: str
    ADDRESSES: Addresses
    DEFAULT_ADDRESS: str
    ADDRESS_TYPES: Optional[AddressTypes] = None
    DEFAULT_ADDRESS_TYPE: Optional[str] = None
    ADDRESS_PREFIXES: Optional[AddressPrefixes] = None
    DEFAULT_ADDRESS_PREFIX: Optional[str] = None
    DEFAULT_SEMANTIC: str = "p2pkh"
    PARAMS: Optional[Params] = None
