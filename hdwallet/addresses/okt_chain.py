#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Any, Union
)

from ..libs.bech32 import (
    bech32_encode, bech32_decode
)
from ..ecc import IPublicKey
from ..cryptocurrencies import OKTChain
from ..utils import (
    get_bytes, bytes_to_string
)
from .ethereum import EthereumAddress
from .iaddress import IAddress


class OKTChainAddress(IAddress):

    hrp: str = OKTChain.NETWORKS.MAINNET.HRP

    @staticmethod
    def name() -> str:
        return "OKT-Chain"

    @classmethod
    def encode(cls, public_key: Union[bytes, str, IPublicKey], **kwargs: Any) -> str:

        return bech32_encode(
            cls.hrp, get_bytes(EthereumAddress.encode(
                public_key, skip_checksum_encode=True
            )[2:])  # remove "0x" at the beginning
        )

    @classmethod
    def decode(cls, address: str, **kwargs: Any) -> str:

        return EthereumAddress.decode(
            EthereumAddress.address_prefix + bytes_to_string(
                bech32_decode(cls.hrp, address)[1]
            ), skip_checksum_encode=True
        )
