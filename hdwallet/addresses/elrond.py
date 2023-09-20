#!/usr/bin/env python3

from typing import (
    Any, Union
)

from ..libs.bech32 import (
    bech32_encode, bech32_decode
)
from ..ecc import (
    IPublicKey, SLIP10Ed25519PublicKey
)
from . import (
    IAddress, validate_and_get_public_key
)


class ElrondAddress(IAddress):

    hrp: str = "erd"

    @classmethod
    def encode(cls, public_key: Union[bytes, str, IPublicKey], **kwargs: Any) -> str:

        public_key: SLIP10Ed25519PublicKey = validate_and_get_public_key(
            public_key=public_key, public_key_cls=SLIP10Ed25519PublicKey
        )
        return bech32_encode(
            kwargs.get("hrp", cls.hrp), public_key.raw_compressed()[1:]
        )

    @classmethod
    def decode(cls, address: str, **kwargs: Any) -> str:

        address_decode_bytes: tuple = bech32_decode(
            kwargs.get("hrp", cls.hrp), address
        )
        return bytearray(
            address_decode_bytes[1]
        ).hex()
