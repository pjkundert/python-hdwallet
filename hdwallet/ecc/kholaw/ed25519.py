#!/usr/bin/env python3

from typing import Any
from nacl import signing

from ..slip10.ed25519 import (
    SLIP10Ed25519Point,
    SLIP10Ed25519PublicKey,
    SLIP10Ed25519PrivateKey,
    CURVE_ORDER,
    GENERATOR
)
from ..ecc import (
    IPoint, IPublicKey, IPrivateKey, EllipticCurveCryptography
)
from ...libs.ed25519 import point_scalar_mul_base

# Private key length in bytes
PRIVATE_KEY_BYTE_LENGTH: int = 64


class KholawEd25519Point(SLIP10Ed25519Point):

    @staticmethod
    def curve_type() -> str:
        return "Kholaw-Ed25519"


class KholawEd25519PublicKey(SLIP10Ed25519PublicKey):

    m_ver_key: signing.VerifyKey

    @staticmethod
    def curve_type() -> str:
        return "Kholaw-Ed25519"

    def point(self) -> IPoint:
        return KholawEd25519Point(bytes(self.m_ver_key))


class KholawEd25519PrivateKey(IPrivateKey):

    m_sign_key: SLIP10Ed25519PrivateKey
    m_ext_key: bytes

    def __init__(self, key_obj: IPrivateKey, key_ex_bytes: bytes) -> None:
        if not isinstance(key_obj, SLIP10Ed25519PrivateKey):
            raise TypeError("Invalid private key object type")
        if len(key_ex_bytes) != SLIP10Ed25519PrivateKey.length():
            raise ValueError("Invalid extended key length")

        self.m_sign_key = key_obj
        self.m_ext_key = key_ex_bytes

    @classmethod
    def from_bytes(cls, key_bytes: bytes) -> IPrivateKey:
        return cls(
            SLIP10Ed25519PrivateKey.from_bytes(
                key_bytes[:SLIP10Ed25519PrivateKey.length()]
            ),
            key_bytes[SLIP10Ed25519PrivateKey.length():]
        )

    @staticmethod
    def curve_type() -> str:
        return "Kholaw-Ed25519"

    @staticmethod
    def length() -> int:
        return PRIVATE_KEY_BYTE_LENGTH

    def underlying_object(self) -> Any:
        return self.m_sign_key.underlying_object()

    def raw(self) -> bytes:
        return self.m_sign_key.raw() + self.m_ext_key

    def public_key(self) -> IPublicKey:
        return KholawEd25519PublicKey(
            signing.VerifyKey(
                point_scalar_mul_base(bytes(self.m_sign_key.underlying_object()))
            )
        )


KholawEd25519: EllipticCurveCryptography = EllipticCurveCryptography(
    "Kholaw-Ed25519", CURVE_ORDER, GENERATOR, KholawEd25519Point, KholawEd25519PublicKey, KholawEd25519PrivateKey
)
