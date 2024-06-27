#!/usr/bin/env python3

from typing import Any
from ecdsa import SigningKey
from ecdsa import (
    curves, keys
)

import coincurve

from ....const import SLIP10_SECP256K1_CONST
from ...iecc import (
    IPublicKey, IPrivateKey
)
from .public_key import (
    SLIP10Secp256k1PublicKeyCoincurve, SLIP10Secp256k1PublicKeyECDSA
)


class SLIP10Secp256k1PrivateKeyCoincurve(IPrivateKey):

    signing_key: coincurve.PrivateKey

    def __init__(self, private_key: coincurve.PrivateKey) -> None:
        self.signing_key = private_key

    @staticmethod
    def name() -> str:
        return "SLIP10-Secp256k1"

    @classmethod
    def from_bytes(cls, private_key: bytes) -> IPrivateKey:
        if len(private_key) != cls.length():
            raise ValueError("Invalid private key bytes")

        try:
            return cls(coincurve.PrivateKey(private_key))
        except ValueError as ex:
            raise ValueError("Invalid private key bytes") from ex

    @staticmethod
    def length() -> int:
        return SLIP10_SECP256K1_CONST.PRIVATE_KEY_BYTE_LENGTH

    def underlying_object(self) -> Any:
        return self.signing_key

    def raw(self) -> bytes:
        return self.signing_key.secret

    def public_key(self) -> IPublicKey:
        return SLIP10Secp256k1PublicKeyCoincurve(self.signing_key.public_key)


class SLIP10Secp256k1PrivateKeyECDSA(IPrivateKey):

    signing_key: SigningKey

    def __init__(self, signing_key: SigningKey) -> None:
        self.signing_key = signing_key

    @staticmethod
    def name() -> str:
        return "SLIP10-Secp256k1"

    @classmethod
    def from_bytes(cls, key_bytes: bytes) -> IPrivateKey:
        try:
            return cls(
                SigningKey.from_string(
                    key_bytes, curve=curves.SECP256k1
                )
            )
        except keys.MalformedPointError as ex:
            raise ValueError("Invalid private key bytes") from ex

    @staticmethod
    def length() -> int:
        return SLIP10_SECP256K1_CONST.PRIVATE_KEY_BYTE_LENGTH

    def underlying_object(self) -> Any:
        return self.signing_key

    def raw(self) -> bytes:
        return self.signing_key.to_string()

    def public_key(self) -> IPublicKey:
        return SLIP10Secp256k1PublicKeyECDSA(self.signing_key.get_verifying_key())


if SLIP10_SECP256K1_CONST.USE == "coincurve":
    SLIP10Secp256k1PrivateKey = SLIP10Secp256k1PrivateKeyCoincurve
elif SLIP10_SECP256K1_CONST.USE == "ecdsa":
    SLIP10Secp256k1PrivateKey = SLIP10Secp256k1PrivateKeyECDSA
else:
    raise Exception(
        f"Invalid SLIP10-Secp256k1 use, (expected: 'coincurve' or 'ecdsa', got: '{SLIP10_SECP256K1_CONST.USE}')"
    )
