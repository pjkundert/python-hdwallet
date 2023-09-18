#!/usr/bin/env python3

from typing import (
    Any, Union
)
from Crypto.Hash import keccak

from ..ecc import (
    IPublicKey, SLIP10Secp256k1PublicKey
)
from . import (
    IAddress, validate_and_get_public_key
)


class EthereumAddress(IAddress):

    address_prefix: str = "0x"

    @staticmethod
    def checksum_encode(address: str) -> str:
        output: str = ""
        keccak_256 = keccak.new(digest_bits=256)
        keccak_256.update(address.lower().encode())
        hash_addr = keccak_256.hexdigest()
        for i, c in enumerate(address):
            if int(hash_addr[i], 16) >= 8:
                output += c.upper()
            else:
                output += c
        return output

    @classmethod
    def encode(cls, public_key: Union[bytes, str, IPublicKey], **kwargs: Any) -> str:

        public_key: SLIP10Secp256k1PublicKey = validate_and_get_public_key(
            public_key=public_key, public_key_cls=SLIP10Secp256k1PublicKey
        )
        keccak_256 = keccak.new(digest_bits=256)
        keccak_256.update(public_key.raw_uncompressed()[1:])
        address = keccak_256.hexdigest()[24:]
        return cls.address_prefix + (
            address if kwargs.get("skip_checksum_encode", False) else cls.checksum_encode(address)
        )

    @classmethod
    def decode(cls, address: str, **kwargs: Any) -> str:

        address_prefix_got: str = address[:len(cls.address_prefix)]
        if cls.address_prefix != address_prefix_got:
            raise ValueError(f"Invalid address_prefix (expected {cls.address_prefix!r}, got {address_prefix_got!r})")
        address_no_prefix = address[len(cls.address_prefix):]

        if len(address_no_prefix) != 40:
            raise ValueError(f"Invalid length (expected {40}, got {len(address_no_prefix)})")
        # Check checksum encoding
        if not kwargs.get("skip_checksum_encode", False) and address_no_prefix != cls.checksum_encode(address_no_prefix):
            print(address_no_prefix, cls.checksum_encode(address_no_prefix))
            raise ValueError("Invalid checksum encode")

        return address_no_prefix.lower()
