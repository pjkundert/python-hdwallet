#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Any, Union
)

from ..ecc import IPublicKey
from ..cryptocurrencies import Avalanche
from ..exceptions import AddressError
from .cosmos import CosmosAddress
from .iaddress import IAddress


class AvalancheAddress(IAddress):

    hrp: str = Avalanche.NETWORKS.MAINNET.HRP
    address_types: dict = {
        "p-chain": Avalanche.PARAMS.ADDRESS_TYPES.P_CHAIN,
        "x-chain": Avalanche.PARAMS.ADDRESS_TYPES.X_CHAIN
    }

    @staticmethod
    def name() -> str:
        return "Avalanche"

    @classmethod
    def encode(cls, public_key: Union[bytes, str, IPublicKey], **kwargs: Any) -> str:

        if not kwargs.get("address_type"):
            address_type: str = cls.address_types[Avalanche.DEFAULT_ADDRESS_TYPE]
        else:
            if kwargs.get("address_type") not in Avalanche.ADDRESS_TYPES.get_address_types():
                raise AddressError(
                    f"Invalid {cls.name()} address type",
                    expected=Avalanche.ADDRESS_TYPES.get_address_types(),
                    got=kwargs.get("address_type")
                )
            address_type: str = cls.address_types[kwargs.get("address_type")]

        return address_type + CosmosAddress.encode(
            public_key=public_key, hrp=cls.hrp
        )

    @classmethod
    def decode(cls, address: str, **kwargs: Any) -> str:

        if not kwargs.get("address_type"):
            address_type: str = cls.address_types[Avalanche.DEFAULT_ADDRESS_TYPE]
        else:
            if kwargs.get("address_type") not in Avalanche.ADDRESS_TYPES.get_address_types():
                raise AddressError(
                    f"Invalid {cls.name()} address type",
                    expected=Avalanche.ADDRESS_TYPES.get_address_types(),
                    got=kwargs.get("address_type")
                )
            address_type: str = cls.address_types[kwargs.get("address_type")]

        prefix_got: str = address[:len(address_type)]
        if address_type != prefix_got:
            raise ValueError(f"Invalid prefix (expected: {address_type}, got: {prefix_got})")
        address_no_prefix: str = address[len(address_type):]

        return CosmosAddress.decode(
            address=address_no_prefix, hrp=cls.hrp
        )
