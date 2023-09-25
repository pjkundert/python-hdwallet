#!/usr/bin/env python3

from typing import (
    Any, Union
)
from hashlib import sha256

from ..libs.bech32 import (
    bech32_encode, bech32_decode
)
from ..ecc import (
    IPublicKey, SLIP10Secp256k1PublicKey
)
from ..utils import bytes_to_string
from . import (
    IAddress, validate_and_get_public_key
)


class ZilliqaAddress(IAddress):

    hrp: str = "zil"
    sha256_byte_length: int = 20

    @classmethod
    def encode(cls, public_key: Union[bytes, str, IPublicKey], **kwargs: Any) -> str:

        public_key: SLIP10Secp256k1PublicKey = validate_and_get_public_key(
            public_key=public_key, public_key_cls=SLIP10Secp256k1PublicKey
        )
        public_key_hash: bytes = sha256(public_key.raw_compressed()).digest()

        return bech32_encode(
            kwargs.get("hrp", cls.hrp), public_key_hash[-cls.sha256_byte_length:]
        )

    @classmethod
    def decode(cls, address: str, **kwargs: Any) -> str:

        hrp, address_decode = bech32_decode(
            kwargs.get("hrp", cls.hrp), address
        )

        if len(address_decode) != cls.sha256_byte_length:
            raise ValueError(f"Invalid length (expected {cls.sha256_byte_length}, got {len(address_decode)})")

        return bytes_to_string(address_decode)
