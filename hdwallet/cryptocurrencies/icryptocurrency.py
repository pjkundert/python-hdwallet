#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from types import SimpleNamespace
from typing import (
    Any, Optional, List, Dict
)

import inspect
import sys

from ..ecc import EllipticCurveCryptography
from ..exceptions import (
    NetworkError, SymbolError
)


class NestedNamespace(SimpleNamespace):

    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, NestedNamespace(value))
            else:
                self.__setattr__(key, value)


class CoinType(NestedNamespace):

    INDEX: int
    HARDENED: bool

    def __str__(self):
        return f"{self.INDEX}'" if self.HARDENED else f"{self.INDEX}"


TESTNET_COIN_TYPE = CoinType({
    "INDEX": 1,
    "HARDENED": True
})


class SegwitAddress(NestedNamespace):

    HRP: Optional[str]
    VERSION: int


class ExtendedKey(NestedNamespace):

    P2PKH: int
    P2SH: int

    P2WPKH: Optional[int] = None
    P2WPKH_IN_P2SH: Optional[int] = None

    P2WSH: Optional[int] = None
    P2WSH_IN_P2SH: Optional[int] = None


class ExtendedPrivateKey(ExtendedKey):
    pass


class ExtendedPublicKey(ExtendedKey):
    pass


class Secp65k1Network(NestedNamespace):

    PUBLIC_KEY_ADDRESS_PREFIX: int
    SCRIPT_ADDRESS_PREFIX: int
    SEGWIT_ADDRESS_PREFIX: SegwitAddress
    DEFAULT_PATH: str
    EXTENDED_PRIVATE_KEY: ExtendedPrivateKey
    EXTENDED_PUBLIC_KEY: ExtendedPublicKey
    WIF_PREFIX: int


class Networks:

    AVAILABLE_NETWORKS: List[Dict[str, Any]]


class Cryptocurrency(NestedNamespace):

    NAME: str
    SYMBOL: str
    NETWORKS: Networks
    SOURCE_CODE: Optional[str]
    ECC: EllipticCurveCryptography
    COIN_TYPE: CoinType
    MESSAGE_PREFIX: Optional[str]

    @classmethod
    def get_network(cls, network: str) -> Any:
        for available_network in cls.NETWORKS.AVAILABLE_NETWORKS:
            if available_network[network]:
                return available_network[network]
        raise NetworkError(f"'{network} network is not available")


def get_cryptocurrency(symbol: str) -> Cryptocurrency:

    for _, cryptocurrency in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(cryptocurrency):
            if issubclass(cryptocurrency, Cryptocurrency) and cryptocurrency != Cryptocurrency:
                if symbol == cryptocurrency.SYMBOL:
                    return cryptocurrency

    raise SymbolError(f"Unknown cryptocurrency '{symbol}' symbol")
