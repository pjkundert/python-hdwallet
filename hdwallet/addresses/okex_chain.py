#!/usr/bin/env python3

from binascii import unhexlify
from typing import (
    Any, Union
)

from ..libs.bech32 import (
    bech32_encode, bech32_decode
)
from ..ecc import IPublicKey
from .ethereum import EthereumAddress
from . import IAddress


class OKExChainAddress(IAddress):

    hrp: str = "ex"

    @classmethod
    def encode(cls, public_key: Union[bytes, str, IPublicKey], **kwargs: Any) -> str:

        return bech32_encode(
            cls.hrp, unhexlify(EthereumAddress.encode(
                public_key, skip_checksum_encode=True
            )[2:])  # remove "0x" at the beginning
        )

    @classmethod
    def decode(cls, address: str, **kwargs: Any) -> str:

        return EthereumAddress.decode(
            EthereumAddress.address_prefix + bytearray(
                bech32_decode(cls.hrp, address)[1]
            ).hex(), skip_checksum_encode=True
        )
