#!/usr/bin/env python3

from typing import (
    Optional, Union
)
from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import PBKDF2

import binascii
import crcmod.predefined
import hashlib

from .libs.ripemd160 import ripemd160 as r160
from .utils import (
    get_bytes, encode, integer_to_bytes
)


def sha256(data: Union[str, bytes]) -> bytes:
    return hashlib.sha256(get_bytes(data)).digest()


def double_sha256(data: Union[str, bytes]) -> bytes:
    return hashlib.sha256(sha256(data)).digest()


def hash160(data: Union[str, bytes]) -> bytes:
    return ripemd160(sha256(data))


def crc32(data: Union[bytes, str]) -> bytes:
    return integer_to_bytes(
        binascii.crc32(encode(data)), bytes_num=4
    )


def xmodem_crc(data: Union[bytes, str]) -> bytes:
    xmodem = crcmod.predefined.Crc("xmodem")
    return xmodem.new(encode(data)).digest()


def pbkdf2_hmac_sha512(
    password: Union[bytes, str], salt: Union[bytes, str], iteration_num: int, derived_key_length: Optional[int] = None
) -> bytes:
    if hasattr(hashlib, "pbkdf2_hmac"):
        return hashlib.pbkdf2_hmac("sha512", encode(password), encode(salt), iteration_num, derived_key_length)
    return PBKDF2(
        password, encode(salt), derived_key_length or SHA512.digest_size, count=iteration_num, hmac_hash_module=SHA512
    )


def ripemd160(data: Union[str, bytes]) -> bytes:
    return (
        hashlib.new("ripemd160", get_bytes(data)).digest()
        if "ripemd160" in hashlib.algorithms_available else
        r160(get_bytes(data))
    )


def sha512_256(data: Union[str, bytes]) -> bytes:
    if "sha512_256" in hashlib.algorithms_available:
        return hashlib.new("sha512_256", encode(data)).digest()
    return SHA512.new(encode(data), truncate="256").digest()
