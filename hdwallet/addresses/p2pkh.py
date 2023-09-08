#!/usr/bin/env python3

from binascii import unhexlify
from typing import (
    Any, Union
)
from hashlib import sha256
from Crypto.Hash import RIPEMD160

import base58
import binascii

from ..libs.base58 import ensure_string
from ..libs.ripemd160 import ripemd160
from ..ecc import (
    IPublicKey, SLIP10Secp256k1PublicKey
)
from . import (
    IAddress, validate_and_get_public_key
)


class P2PKHAddress(IAddress):
    
    network_version: int = 0x00
    alphabet: bytes = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

    @classmethod
    def encode(cls, public_key: Union[bytes, str, IPublicKey], **kwargs: Any) -> str:
        try:
            network_version: bytes = unhexlify("0%x" % kwargs.get("network_version", cls.network_version))
        except binascii.Error:
            network_version: bytes = unhexlify("%x" % kwargs.get("network_version", cls.network_version))

        public_key: SLIP10Secp256k1PublicKey = validate_and_get_public_key(
            public_key=public_key, public_key_cls=SLIP10Secp256k1PublicKey
        )
        public_key_hash: bytes = ripemd160(sha256(
            public_key.raw_compressed() if kwargs.get("public_key_mode", "compressed") == "compressed" else public_key.raw_uncompressed()
        ).digest())

        return ensure_string(base58.b58encode_check(
            (network_version + public_key_hash), alphabet=kwargs.get(
                "alphabet", cls.alphabet
            )
        ))

    @classmethod
    def decode(cls, address: str, **kwargs: Any) -> str:
        try:
            network_version: bytes = unhexlify("0%x" % kwargs.get("network_version", cls.network_version))
        except binascii.Error:
            network_version: bytes = unhexlify("%x" % kwargs.get("network_version", cls.network_version))

        address_decode: bytes = base58.b58decode_check(
            address, alphabet=kwargs.get(
                "alphabet", cls.alphabet
            )
        )

        if len(address_decode) != RIPEMD160.digest_size + len(network_version):
            raise ValueError(f"Invalid length (expected {RIPEMD160.digest_size + len(network_version)}, got {len(address_decode)})")

        prefix_got: bytes = address_decode[:len(network_version)]
        if network_version != prefix_got:
            raise ValueError(f"Invalid prefix (expected {network_version!r}, got {prefix_got!r})")
        return address_decode[len(network_version):].hex()
