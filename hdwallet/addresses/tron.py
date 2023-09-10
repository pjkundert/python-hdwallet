#!/usr/bin/env python3

from binascii import unhexlify
from typing import (
    Any, Union
)
from Crypto.Hash import keccak

import binascii
import base58

from ..libs.base58 import ensure_string
from ..ecc import (
    IPublicKey, SLIP10Secp256k1PublicKey
)
from .p2pkh import P2PKHAddress
from . import validate_and_get_public_key


class TronAddress(P2PKHAddress):

    public_key_address: int = 0x41
    alphabet: bytes = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

    @classmethod
    def encode(cls, public_key: Union[bytes, str, IPublicKey], **kwargs: Any) -> str:

        public_key: SLIP10Secp256k1PublicKey = validate_and_get_public_key(
            public_key=public_key, public_key_cls=SLIP10Secp256k1PublicKey
        )
        keccak_256 = keccak.new(digest_bits=256)
        keccak_256.update(public_key.raw_uncompressed()[1:])
        address = keccak_256.hexdigest()[24:]

        try:
            network_version: bytes = unhexlify("0%x" % cls.public_key_address)
        except binascii.Error:
            network_version: bytes = unhexlify("%x" % cls.public_key_address)

        return ensure_string(base58.b58encode_check(
            (network_version + bytearray.fromhex(address)), alphabet=kwargs.get(
                "alphabet", cls.alphabet
            )
        ))

    @classmethod
    def decode(cls, address: str, **kwargs: Any) -> str:
        try:
            network_version: bytes = unhexlify("0%x" % cls.public_key_address)
        except binascii.Error:
            network_version: bytes = unhexlify("%x" % cls.public_key_address)

        address_decode_bytes: bytes = base58.b58decode_check(
            address, alphabet=kwargs.get(
                "alphabet", cls.alphabet
            )
        )

        if len(address_decode_bytes) != 20 + len(network_version):
            raise ValueError(f"Invalid length (expected {20 + len(network_version)}, got {len(address_decode_bytes)})")

        prefix_got: bytes = address_decode_bytes[:len(network_version)]
        if network_version != prefix_got:
            raise ValueError(f"Invalid prefix (expected {network_version!r}, got {prefix_got!r})")
        return address_decode_bytes[len(network_version):].hex()
