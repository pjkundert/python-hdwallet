#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Optional, Union, Literal, List, Any
)
from types import SimpleNamespace

from .exceptions import NetworkError
from .utils import bytes_to_integer


class NestedNamespace(SimpleNamespace):

    def __init__(self, data: Union[set, tuple, dict], **kwargs):
        super().__init__(**kwargs)
        if isinstance(data, set):
            for item in data:
                self.__setattr__(item, item)
        if isinstance(data, tuple):
            for item in data:
                if isinstance(item, dict):
                    for key, value in item.items():
                        if isinstance(value, dict):
                            self.__setattr__(key, NestedNamespace(value))
                        else:
                            self.__setattr__(key, value)
                else:
                    self.__setattr__(item, item)
        elif isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    self.__setattr__(key, NestedNamespace(value))
                else:
                    self.__setattr__(key, value)


class Ed25519Const(NestedNamespace):

    PRIVATE_KEY_BYTE_LENGTH: int
    PUBLIC_KEY_PREFIX: bytes
    PUBLIC_KEY_BYTE_LENGTH: int


SLIP10_ED25519_CONST: Ed25519Const = Ed25519Const({
    "PRIVATE_KEY_BYTE_LENGTH": 32,
    "PUBLIC_KEY_PREFIX": b"\x00",
    "PUBLIC_KEY_BYTE_LENGTH": 32
})


KHOLAW_ED25519_CONST: Ed25519Const = Ed25519Const({
    "PRIVATE_KEY_BYTE_LENGTH": 64,
    "PUBLIC_KEY_PREFIX": b"\x00",
    "PUBLIC_KEY_BYTE_LENGTH": 32
})


class Secp256k1Const(NestedNamespace):

    USE: Literal["coincurve", "ecdsa"]
    POINT_COORDINATE_BYTE_LENGTH: int
    PRIVATE_KEY_BYTE_LENGTH: int
    PUBLIC_KEY_UNCOMPRESSED_PREFIX: bytes
    PUBLIC_KEY_COMPRESSED_BYTE_LENGTH: int
    PUBLIC_KEY_UNCOMPRESSED_BYTE_LENGTH: int


SLIP10_SECP256K1_CONST: Secp256k1Const = Secp256k1Const({
    "USE": "coincurve",
    "POINT_COORDINATE_BYTE_LENGTH": 32,
    "PRIVATE_KEY_BYTE_LENGTH": 32,
    "PUBLIC_KEY_UNCOMPRESSED_PREFIX": b"\x04",
    "PUBLIC_KEY_COMPRESSED_BYTE_LENGTH": 33,
    "PUBLIC_KEY_UNCOMPRESSED_BYTE_LENGTH": 65,
})


class CoinType(NestedNamespace):

    INDEX: int
    HARDENED: bool

    def __str__(self) -> str:
        return f"{self.INDEX}'" if self.HARDENED else f"{self.INDEX}"

    def __int__(self) -> int:
        return self.INDEX


class WitnessVersions(NestedNamespace):

    def get_witness_version(self, address: str) -> int:
        return self.__getattribute__(address.upper())


class Entropies(NestedNamespace):

    def get_entropies(self) -> List[str]:
        return list(self.__dict__.values())


class Mnemonics(NestedNamespace):

    def get_mnemonics(self) -> List[str]:
        return list(self.__dict__.values())


class Seeds(NestedNamespace):

    def get_seeds(self) -> List[str]:
        return list(self.__dict__.values())


class HDs(NestedNamespace):

    def get_hds(self) -> List[str]:
        return list(self.__dict__.values())


class Addresses(NestedNamespace):

    def get_addresses(self) -> List[str]:
        return list(self.__dict__.values())


class Networks(NestedNamespace):

    def is_network(self, network: str) -> bool:
        return network in self.get_networks()

    def get_networks(self) -> List[str]:
        return [network.lower() for network in self.__dict__.keys()]

    def get_network(self, network: str) -> Any:  # INetwork
        if not self.is_network(network=network):
            raise NetworkError(f"'{network} network is not available")

        return self.__getattribute__(network.upper())


class Params(NestedNamespace):
    pass


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


class XPrivateKeyVersions(ExtendedKeyVersions):
    pass


class XPublicKeyVersions(ExtendedKeyVersions):
    pass


class PublicKeyTypes(NestedNamespace):

    UNCOMPRESSED: str
    COMPRESSED: str

    def get_types(self) -> List[str]:
        return [
            self.UNCOMPRESSED, self.COMPRESSED
        ]


PUBLIC_KEY_TYPES: PublicKeyTypes = PublicKeyTypes({
    "UNCOMPRESSED": "uncompressed",
    "COMPRESSED": "compressed"
})


class WIFTypes(NestedNamespace):

    WIF: str
    WIF_COMPRESSED: str

    def get_types(self) -> List[str]:
        return [
            self.WIF, self.WIF_COMPRESSED
        ]


WIF_TYPES: WIFTypes = WIFTypes({
    "WIF": "wif",
    "WIF_COMPRESSED": "wif-compressed"
})


class ElectrumV2Modes(NestedNamespace):

    STANDARD: str
    SEGWIT: str

    def get_modes(self) -> List[str]:
        return [
            self.STANDARD, self.SEGWIT
        ]


ELECTRUM_V2_MODES: ElectrumV2Modes = ElectrumV2Modes({
    "STANDARD": "standard",
    "SEGWIT": "segwit"
})
