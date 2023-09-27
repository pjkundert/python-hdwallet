#!/usr/bin/env python3

from typing import (
    Any, Union
)

from ..ecc import (
    IPublicKey, SLIP10Secp256k1PublicKey
)
from ..crypto import kekkak256
from ..utils import bytes_to_string
from . import (
    IAddress, validate_and_get_public_key
)


class EthereumAddress(IAddress):

    address_prefix: str = "0x"

    @staticmethod
    def checksum_encode(address: str) -> str:
        output: str = ""
        address_hash: str = bytes_to_string(
            kekkak256(address.lower())
        )
        for i, c in enumerate(address):
            if int(address_hash[i], 16) >= 8:
                output += c.upper()
            else:
                output += c
        return output

    @classmethod
    def encode(cls, public_key: Union[bytes, str, IPublicKey], **kwargs: Any) -> str:

        public_key: SLIP10Secp256k1PublicKey = validate_and_get_public_key(
            public_key=public_key, public_key_cls=SLIP10Secp256k1PublicKey
        )
        address: str = bytes_to_string(
            kekkak256(public_key.raw_uncompressed()[1:])
        )[24:]
        return cls.address_prefix + (
            address if kwargs.get("skip_checksum_encode", False) else cls.checksum_encode(address)
        )

    @classmethod
    def decode(cls, address: str, **kwargs: Any) -> str:

        address_prefix_got: str = address[:len(cls.address_prefix)]
        if cls.address_prefix != address_prefix_got:
            raise ValueError(f"Invalid address_prefix (expected: {cls.address_prefix}, got: {address_prefix_got})")
        address_no_prefix = address[len(cls.address_prefix):]

        if len(address_no_prefix) != 40:
            raise ValueError(f"Invalid length (expected: {40}, got: {len(address_no_prefix)})")
        # Check checksum encoding
        if not kwargs.get("skip_checksum_encode", False) and address_no_prefix != cls.checksum_encode(address_no_prefix):
            print(address_no_prefix, cls.checksum_encode(address_no_prefix))
            raise ValueError("Invalid checksum encode")

        return address_no_prefix.lower()
