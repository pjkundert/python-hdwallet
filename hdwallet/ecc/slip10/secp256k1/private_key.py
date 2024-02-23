#!/usr/bin/env python3

from typing import Any
from ecdsa import (
    curves, keys
)

import coincurve
import ecdsa

from ....const import SLIP10_SECP256K1_CONST
from ...iecc import (
    IPublicKey, IPrivateKey
)
from .public_key import SLIP10Secp256k1PublicKey


if SLIP10_SECP256K1_CONST.USE == "coincurve":

    class SLIP10Secp256k1PrivateKey(IPrivateKey):

        m_sign_key: coincurve.PrivateKey

        def __init__(self, key_obj: coincurve.PrivateKey) -> None:
            self.m_sign_key = key_obj

        @classmethod
        def from_bytes(cls, key_bytes: bytes) -> IPrivateKey:
            if len(key_bytes) != cls.length():
                raise ValueError("Invalid private key bytes")

            try:
                return cls(coincurve.PrivateKey(key_bytes))
            except ValueError as ex:
                raise ValueError("Invalid private key bytes") from ex

        @staticmethod
        def curve_type() -> str:
            return "SLIP10-Secp256k1"

        @staticmethod
        def length() -> int:
            return SLIP10_SECP256K1_CONST.PRIVATE_KEY_BYTE_LENGTH

        def underlying_object(self) -> Any:
            return self.m_sign_key

        def raw(self) -> bytes:
            return self.m_sign_key.secret

        def public_key(self) -> IPublicKey:
            return SLIP10Secp256k1PublicKey(self.m_sign_key.public_key)

elif SLIP10_SECP256K1_CONST.USE == "ecdsa":

    class SLIP10Secp256k1PrivateKey(IPrivateKey):
        m_sign_key = ecdsa.SigningKey

        def __init__(self, key_obj: ecdsa.SigningKey) -> None:
            self.m_sign_key = key_obj

        @classmethod
        def from_bytes(cls, key_bytes: bytes) -> IPrivateKey:
            try:
                return cls(
                    ecdsa.SigningKey.from_string(
                        key_bytes, curve=curves.SECP256k1
                    )
                )
            except keys.MalformedPointError as ex:
                raise ValueError("Invalid private key bytes") from ex

        @staticmethod
        def curve_type() -> str:
            return "SLIP10-Secp256k1"

        @staticmethod
        def length() -> int:
            return SLIP10_SECP256K1_CONST.PRIVATE_KEY_BYTE_LENGTH

        def underlying_object(self) -> Any:
            return self.m_sign_key

        def raw(self) -> bytes:
            return self.m_sign_key.to_string()

        def public_key(self) -> IPublicKey:
            return SLIP10Secp256k1PublicKey(self.m_sign_key.get_verifying_key())

else:
    Exception(
        f"Invalid SLIP10-Secp256k1 use, (expected: 'coincurve' or 'ecdsa', got: '{SLIP10_SECP256K1_CONST.USE}')"
    )
