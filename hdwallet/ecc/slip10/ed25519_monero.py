#!/usr/bin/env python3

from nacl import signing

from .ed25519 import (
    SLIP10Ed25519Point,
    SLIP10Ed25519PublicKey,
    SLIP10Ed25519PrivateKey,
    CURVE_ORDER,
    GENERATOR,
    PUBLIC_KEY_BYTE_LENGTH
)
from ..ecc import (
    IPoint, IPublicKey, IPrivateKey, EllipticCurveCryptography
)
from ...libs.ed25519 import (
    scalar_is_valid, point_scalar_mul_base
)


class SLIP10Ed25519MoneroPoint(SLIP10Ed25519Point):

    @staticmethod
    def curve_type() -> str:
        return "SLIP10-Ed25519-Monero"


class SLIP10Ed25519MoneroPublicKey(SLIP10Ed25519PublicKey):

    @staticmethod
    def curve_type() -> str:
        return "SLIP10-Ed25519-Monero"

    @staticmethod
    def compressed_length() -> int:
        return PUBLIC_KEY_BYTE_LENGTH

    @staticmethod
    def uncompressed_length() -> int:
        return SLIP10Ed25519MoneroPublicKey.compressed_length()

    def raw_compressed(self) -> bytes:
        return bytes(self.m_ver_key)

    def raw_uncompressed(self) -> bytes:
        return self.raw_compressed()

    def point(self) -> IPoint:
        return SLIP10Ed25519Point(bytes(self.m_ver_key))


class SLIP10Ed25519MoneroPrivateKey(SLIP10Ed25519PrivateKey):

    @classmethod
    def from_bytes(cls, key_bytes: bytes) -> IPrivateKey:
        if not scalar_is_valid(key_bytes):
            raise ValueError("Invalid private key bytes")
        return super().from_bytes(key_bytes)

    @staticmethod
    def curve_type() -> str:
        return "SLIP10-Ed25519-Monero"

    def public_key(self) -> IPublicKey:
        return SLIP10Ed25519MoneroPublicKey(
            signing.VerifyKey(
                point_scalar_mul_base(bytes(self.m_sign_key))
            )
        )


SLIP10Ed25519Monero: EllipticCurveCryptography = EllipticCurveCryptography(
    "SLIP10-Ed25519-Monero", CURVE_ORDER, GENERATOR, SLIP10Ed25519MoneroPoint, SLIP10Ed25519MoneroPublicKey, SLIP10Ed25519MoneroPrivateKey
)
