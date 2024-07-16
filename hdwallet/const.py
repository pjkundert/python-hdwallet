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


class SLIP10_ED25519_CONST:
    """
    ``SLIP10-ED25519`` Constants.
    
    +-------------------------+-----------+--------------+
    | Name                    | Type      | Value        |
    +=========================+===========+==============+
    | PRIVATE_KEY_BYTE_LENGTH | ``int``   | 32           |
    +-------------------------+-----------+--------------+
    | PUBLIC_KEY_PREFIX       | ``bytes`` | ``0x00``     |
    +-------------------------+-----------+--------------+
    | PUBLIC_KEY_BYTE_LENGTH  | ``int``   | 32           |
    +-------------------------+-----------+--------------+
    """

    PRIVATE_KEY_BYTE_LENGTH: int = 32
    PUBLIC_KEY_PREFIX: bytes = b"\x00"
    PUBLIC_KEY_BYTE_LENGTH: int = 32


class KHOLAW_ED25519_CONST(SLIP10_ED25519_CONST):
    """
    ``KHOLAW-ED25519`` Constants.
    
    +-------------------------+-----------+--------------+
    | Name                    | Type      | Value        |
    +=========================+===========+==============+
    | PRIVATE_KEY_BYTE_LENGTH | ``int``   | 64           |
    +-------------------------+-----------+--------------+
    | PUBLIC_KEY_PREFIX       | ``bytes`` | ``0x00``     |
    +-------------------------+-----------+--------------+
    | PUBLIC_KEY_BYTE_LENGTH  | ``int``   | 32           |
    +-------------------------+-----------+--------------+
    """

    PRIVATE_KEY_BYTE_LENGTH: int = 64


class SLIP10_SECP256K1_CONST:
    """
    ``SLIP10-SECP256K1`` Constants.
    
    +-------------------------------------+-----------------------------------+-------------+
    | Name                                | Type                              | Value       |
    +=====================================+===================================+=============+
    | USE                                 | ``Literal['coincurve', 'ecdsa']`` | 'coincurve' |
    +-------------------------------------+-----------------------------------+-------------+
    | POINT_COORDINATE_BYTE_LENGTH        | ``int``                           | 32          |
    +-------------------------------------+-----------------------------------+-------------+
    | PRIVATE_KEY_BYTE_LENGTH             | ``int``                           | 32          |
    +-------------------------------------+-----------------------------------+-------------+
    | PUBLIC_KEY_PREFIX                   | ``bytes``                         | ``0x04``    |
    +-------------------------------------+-----------------------------------+-------------+
    | PUBLIC_KEY_COMPRESSED_BYTE_LENGTH   | ``int``                           | 33          |
    +-------------------------------------+-----------------------------------+-------------+
    | PUBLIC_KEY_UNCOMPRESSED_BYTE_LENGTH | ``int``                           | 65          |
    +-------------------------------------+-----------------------------------+-------------+
    """

    USE: Literal["coincurve", "ecdsa"] = "coincurve"
    POINT_COORDINATE_BYTE_LENGTH: int = 32
    PRIVATE_KEY_BYTE_LENGTH: int = 32
    PUBLIC_KEY_UNCOMPRESSED_PREFIX: bytes = b"\x04"
    PUBLIC_KEY_COMPRESSED_BYTE_LENGTH: int = 33
    PUBLIC_KEY_UNCOMPRESSED_BYTE_LENGTH: int = 65


class Info(NestedNamespace):

    SOURCE_CODE: Optional[str]
    WHITEPAPER: Optional[str]
    WEBSITES: List[str]


class WitnessVersions(NestedNamespace):

    def get_witness_version(self, address: str) -> Optional[int]:
        try:
            return self.__getattribute__(address.upper())
        except AttributeError:
            return None


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

    def length(self) -> int:
        return len(self.get_addresses())


class AddressTypes(NestedNamespace):

    def get_address_types(self) -> List[str]:
        return list(self.__dict__.values())


class AddressPrefixes(NestedNamespace):

    def get_address_prefixes(self) -> List[str]:
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


class PUBLIC_KEY_TYPES:
    """
    ``PUBLIC_KEY_TYPES`` Constants.

    +----------------+-----------+-----------------+
    | Name           | Type      | Value           |
    +================+===========+=================+
    | COMPRESSED     | ``str``   | 'uncompressed'  |
    +----------------+-----------+-----------------+
    | UNCOMPRESSED   | ``str``   | 'compressed'    |
    +----------------+-----------+-----------------+
    """

    UNCOMPRESSED: str = "uncompressed"
    COMPRESSED: str = "compressed"

    @classmethod
    def get_types(cls) -> List[str]:
        """
        Get a list of all public key types.

        :return: List of public key types.
        :rtype: List[str]
        """

        return [
            cls.UNCOMPRESSED, cls.COMPRESSED
        ]


class WIF_TYPES:
    """
    ``WIF_TYPES`` Constants.

    +----------------+-----------+------------------+
    | Name           | Type      | Value            |
    +================+===========+==================+
    | WIF            | ``str``   | 'wif'            |
    +----------------+-----------+------------------+
    | WIF_COMPRESSED | ``str``   | 'wif-compressed' |
    +----------------+-----------+------------------+
    """

    WIF: str = "wif"
    WIF_COMPRESSED: str = "wif-compressed"

    @classmethod
    def get_types(cls) -> List[str]:
        """
        Get a list of all WIF types.

        :return: List of WIF types.
        :rtype: List[str]
        """

        return [
            cls.WIF, cls.WIF_COMPRESSED
        ]


class ELECTRUM_V2_MODES:
    """
    ``PUBLIC_KEY_TYPES`` Constants.

    +----------------+-----------+-----------------+
    | Name           | Type      | Value           |
    +================+===========+=================+
    | STANDARD       | ``str``   | 'standard'      |
    +----------------+-----------+-----------------+
    | SEGWIT         | ``str``   | 'segwit'        |
    +----------------+-----------+-----------------+
    """

    STANDARD: str = "standard"
    SEGWIT: str = "segwit"

    @classmethod
    def get_modes(cls) -> List[str]:
        """
        Get a list of all Electrum V2 modes.

        :return: List of Electrum V2 modes.
        :rtype: List[str]
        """

        return [
            cls.STANDARD, cls.SEGWIT
        ]


