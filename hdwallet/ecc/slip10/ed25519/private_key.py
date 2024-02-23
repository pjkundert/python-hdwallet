#!/usr/bin/env python3

from typing import Any
from nacl import (
    exceptions, signing
)

from ....const import SLIP10_ED25519_CONST
from ...iecc import (
    IPublicKey, IPrivateKey
)
from .public_key import SLIP10Ed25519PublicKey


class SLIP10Ed25519PrivateKey(IPrivateKey):

    m_sign_key: signing.SigningKey

    def __init__(self, key_obj: signing.SigningKey) -> None:
        self.m_sign_key = key_obj

    @classmethod
    def from_bytes(cls, key_bytes: bytes) -> IPrivateKey:
        try:
            return cls(signing.SigningKey(key_bytes))
        except (exceptions.RuntimeError, exceptions.ValueError) as ex:
            raise ValueError("Invalid private key bytes") from ex

    @staticmethod
    def curve_type() -> str:
        return "SLIP10-Ed25519"

    @staticmethod
    def length() -> int:
        return SLIP10_ED25519_CONST.PRIVATE_KEY_BYTE_LENGTH

    def underlying_object(self) -> Any:
        return self.m_sign_key

    def raw(self) -> bytes:
        return bytes(self.m_sign_key)

    def public_key(self) -> IPublicKey:
        return SLIP10Ed25519PublicKey(self.m_sign_key.verify_key)
