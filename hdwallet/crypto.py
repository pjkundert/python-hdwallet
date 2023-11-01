#!/usr/bin/env python3

from typing import (
    Optional, Union, Tuple
)
from Crypto.Hash import (
    SHA512, SHA3_256, keccak
)
from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Protocol.KDF import PBKDF2

import binascii
import crcmod.predefined
import hashlib
import hmac

from .libs.ripemd160 import ripemd160 as r160
from .utils import (
    get_bytes, encode, integer_to_bytes
)


def hmac_sha256(key: Union[bytes, str], data: Union[bytes, str]) -> bytes:
    if hasattr(hmac, "digest"):
        return hmac.digest(
            encode(key), encode(data), "sha256"
        )
    return hmac.new(
        encode(key), encode(data), hashlib.sha256
    ).digest()


def hmac_sha512(key: Union[bytes, str], data: Union[bytes, str]) -> bytes:
    if hasattr(hmac, "digest"):
        return hmac.digest(
            encode(key), encode(data), "sha512"
        )
    return hmac.new(
        encode(key), encode(data), hashlib.sha512
    ).digest()


def blake2b(data: Union[bytes, str], digest_size: int, key: Union[bytes, str] = b"", salt: Union[bytes, str] = b"") -> bytes:
    return hashlib.blake2b(
        encode(data), digest_size=digest_size, key=encode(key), salt=encode(salt)
    ).digest()


def blake2b_32(data: Union[bytes, str], key: Union[bytes, str] = b"", salt: Union[bytes, str] = b"") -> bytes:
    return blake2b(data=data, digest_size=4, key=key, salt=salt)


def blake2b_40(data: Union[bytes, str], key: Union[bytes, str] = b"", salt: Union[bytes, str] = b"") -> bytes:
    return blake2b(data=data, digest_size=5, key=key, salt=salt)


def blake2b_160(data: Union[bytes, str], key: Union[bytes, str] = b"", salt: Union[bytes, str] = b"") -> bytes:
    return blake2b(data=data, digest_size=20, key=key, salt=salt)


def blake2b_224(data: Union[bytes, str], key: Union[bytes, str] = b"", salt: Union[bytes, str] = b"") -> bytes:
    return blake2b(data=data, digest_size=28, key=key, salt=salt)


def blake2b_256(data: Union[bytes, str], key: Union[bytes, str] = b"", salt: Union[bytes, str] = b"") -> bytes:
    return blake2b(data=data, digest_size=32, key=key, salt=salt)


def blake2b_512(data: Union[bytes, str], key: Union[bytes, str] = b"", salt: Union[bytes, str] = b"") -> bytes:
    return blake2b(data=data, digest_size=64, key=key, salt=salt)


def chacha20_poly1305_encrypt(
    key: Union[bytes, str], nonce: Union[bytes, str], assoc_data: Union[bytes, str], plain_text: Union[bytes, str]
) -> Tuple[bytes, bytes]:
    cipher: ChaCha20_Poly1305 = ChaCha20_Poly1305.new(
        key=encode(key), nonce=encode(nonce)
    )
    cipher.update(encode(assoc_data))
    return cipher.encrypt_and_digest(encode(plain_text))


def chacha20_poly1305_decrypt(
    key: Union[bytes, str], nonce: Union[bytes, str], assoc_data: Union[bytes, str], cipher_text: Union[bytes, str], tag: Union[bytes, str]
) -> bytes:
    cipher: ChaCha20_Poly1305 = ChaCha20_Poly1305.new(
        key=encode(key), nonce=encode(nonce)
    )
    cipher.update(encode(assoc_data))
    return cipher.decrypt_and_verify(encode(cipher_text), encode(tag))


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


def kekkak256(data: Union[str, bytes]) -> bytes:
    return keccak.new(data=encode(data), digest_bits=256).digest()


def ripemd160(data: Union[str, bytes]) -> bytes:
    if "ripemd160" in hashlib.algorithms_available:
        hashlib.new("ripemd160", get_bytes(data)).digest()
    return r160(get_bytes(data))


def sha512(data: Union[str, bytes]) -> bytes:
    return hashlib.sha512(encode(data)).digest()


def sha512_256(data: Union[str, bytes]) -> bytes:
    if "sha512_256" in hashlib.algorithms_available:
        return hashlib.new("sha512_256", encode(data)).digest()
    return SHA512.new(encode(data), truncate="256").digest()


def sha3_256(data: Union[str, bytes]) -> bytes:
    if "sha3_256" in hashlib.algorithms_available:
        return hashlib.new("sha3_256", encode(data)).digest()
    return SHA3_256.new(encode(data)).digest()
