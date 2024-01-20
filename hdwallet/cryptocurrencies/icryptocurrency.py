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

from ..ecc import EllipticCurveCryptography
from ..entropies import (
    AlgorandEntropy, BIP39Entropy, ElectrumV1Entropy, ElectrumV2Entropy, MoneroEntropy
)
from ..mnemonics import (
    AlgorandMnemonic, BIP39Mnemonic, ElectrumV1Mnemonic, ElectrumV2Mnemonic, MoneroMnemonic
)
from ..seeds import (
    AlgorandSeed, BIP39Seed, CardanoSeed, ElectrumV1Seed, ElectrumV2Seed, MoneroSeed
)
from ..derivations.bip44 import BIP44Derivation
from ..utils import (
    NestedNamespace, bytes_to_integer
)
from ..exceptions import NetworkError


class CoinType(NestedNamespace):

    INDEX: int
    HARDENED: bool

    def __str__(self) -> str:
        return f"{self.INDEX}'" if self.HARDENED else f"{self.INDEX}"

    def __int__(self) -> int:
        return self.INDEX


class SegwitAddress(NestedNamespace):

    HRP: Optional[str]
    VERSION: int


class ExtendedKeyVersions(NestedNamespace):

    def is_version(self, version: bytes) -> bool:
        return bytes_to_integer(version) in self.__dict__.values()

    def get_version(self, name: str) -> Union[str, int, bytes]:
        return self.__getattribute__(name)

    def get_name(self, version: bytes) -> Optional[str]:
        name: Optional[str] = None
        for key in self.__dict__.keys():
            if self.__dict__.get(key) == bytes_to_integer(version):
                name = key
                break
        return name


class ExtendedPrivateKeyVersions(ExtendedKeyVersions):
    pass


class ExtendedPublicKeyVersions(ExtendedKeyVersions):
    pass


class INetwork:

    # Bitcoin network types
    PUBLIC_KEY_ADDRESS_PREFIX: Optional[int] = None
    SCRIPT_ADDRESS_PREFIX: Optional[int] = None
    SEGWIT_ADDRESS_PREFIX: Optional[SegwitAddress] = None
    EXTENDED_PRIVATE_KEY_VERSIONS: Optional[ExtendedPrivateKeyVersions] = None
    EXTENDED_PUBLIC_KEY_VERSIONS: Optional[ExtendedPublicKeyVersions] = None
    MESSAGE_PREFIX: Optional[str] = None
    WIF_PREFIX: Optional[int] = None

    # Monero network types
    STANDARD: Optional[int] = None
    INTEGRATED: Optional[int] = None
    SUB_ADDRESS: Optional[int] = None

    # Cardano network types
    TYPE: Optional[int] = None
    PAYMENT_ADDRESS_HRP: Optional[str] = None
    REWARD_ADDRESS_HRP: Optional[str] = None


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
    ENTROPIES: List[Union[
        AlgorandEntropy, BIP39Entropy, ElectrumV1Entropy, ElectrumV2Entropy, MoneroEntropy
    ]]
    MNEMONICS: List[Union[
        AlgorandMnemonic, BIP39Mnemonic, ElectrumV1Mnemonic, ElectrumV2Mnemonic, MoneroMnemonic
    ]]
    SEEDS: List[Union[
        AlgorandSeed, BIP39Seed, CardanoSeed, ElectrumV1Seed, ElectrumV2Seed, MoneroSeed
    ]]

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
