#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from abc import (
    ABC, abstractmethod
)

from typing import (
    Optional, Union, Type, List
)

import inspect
import sys

from ..ecc import EllipticCurveCryptography
from ..derivations.bip44 import BIP44Derivation
from ..utils import NestedNamespace
from ..exceptions import (
    NetworkError, SymbolError
)


class CoinType(NestedNamespace):

    INDEX: int
    HARDENED: bool

    def __str__(self):
        return f"{self.INDEX}'" if self.HARDENED else f"{self.INDEX}"


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


class INetwork:

    PUBLIC_KEY_ADDRESS_PREFIX: int
    SCRIPT_ADDRESS_PREFIX: int
    SEGWIT_ADDRESS_PREFIX: Optional[SegwitAddress]
    EXTENDED_PRIVATE_KEY: Optional[ExtendedPrivateKey]
    EXTENDED_PUBLIC_KEY: Optional[ExtendedPublicKey]
    MESSAGE_PREFIX: Optional[str]
    WIF_PREFIX: int


class INetworks(ABC):

    @classmethod
    @abstractmethod
    def networks(cls) -> List[str]:
        pass

    @classmethod
    def is_network(cls, network: str) -> bool:
        return network in cls.networks()

    @classmethod
    def get_network(cls, network: str) -> INetwork:

        if not cls.is_network(network=network):
            raise NetworkError(f"'{network} network is not available")

        return cls.__getattribute__(cls, network.upper())


class ICryptocurrency:

    NAME: str
    SYMBOL: str
    NETWORKS: INetworks
    SOURCE_CODE: Optional[str]
    ECC: EllipticCurveCryptography
    COIN_TYPE: CoinType

    @classmethod
    def get_default_path(cls, network: Union[str, Type[INetwork]]) -> str:
        try:
            if not isinstance(network, str) and issubclass(network, INetwork):
                network = network.__name__.lower()
            if not cls.NETWORKS.is_network(network=network):
                raise NetworkError(
                    f"Wrong {cls.NAME} network", expected=cls.NETWORKS.networks(), got=network
                )

            bip44_derivation: BIP44Derivation = BIP44Derivation(
                account=0, change="external-chain", address=0
            )
            bip44_derivation.from_coin_type(
                coin_type=cls.COIN_TYPE.INDEX if network == "mainnet" else 1
            )
            return bip44_derivation.path()
        except TypeError:
            raise NetworkError(
                "Invalid network type", expected=[str, INetwork], got=type(network)
            )


def get_cryptocurrency(symbol: str) -> ICryptocurrency:

    for _, cryptocurrency in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(cryptocurrency):
            if issubclass(cryptocurrency, ICryptocurrency) and cryptocurrency != ICryptocurrency:
                if symbol == cryptocurrency.SYMBOL:
                    return cryptocurrency

    raise SymbolError(f"Unknown cryptocurrency '{symbol}' symbol")
