#!/usr/bin/env python3

from typing import (
    Optional, Any
)
from nacl import (
    exceptions, signing
)

from ..ecc import (
    IPoint, IPublicKey, IPrivateKey, EllipticCurveCryptography
)
from ...libs.ed25519 import (
    point_add,
    int_encode,
    point_encode,
    point_is_encoded_bytes,
    point_is_generator,
    point_is_on_curve,
    point_is_decoded_bytes,
    point_coord_to_bytes,
    point_bytes_to_coord,
    point_scalar_mul_base,
    point_scalar_mul
)
from ...utils import bytes_to_integer

# Public key prefix
PUBLIC_KEY_PREFIX: bytes = b"\x00"
# Public key length in bytes
PUBLIC_KEY_BYTE_LENGTH: int = 32
# Private key length in bytes
PRIVATE_KEY_BYTE_LENGTH: int = 32


class SLIP10Ed25519Point(IPoint):

    m_is_generator: bool
    m_enc_bytes: bytes
    m_x: Optional[int]
    m_y: Optional[int]

    def __init__(self, point_bytes: bytes) -> None:
        if not point_is_encoded_bytes(point_bytes):
            raise ValueError("Invalid point bytes")

        self.m_enc_bytes = point_bytes
        self.m_is_generator = point_is_generator(point_bytes)
        self.m_x, self.m_y = None, None

    @classmethod
    def from_bytes(cls, point_bytes: bytes) -> IPoint:
        if not point_is_on_curve(point_bytes):
            raise ValueError("Invalid point bytes")
        if point_is_decoded_bytes(point_bytes):
            point_bytes = point_encode(
                point_bytes_to_coord(point_bytes)
            )
        return cls(point_bytes)

    @classmethod
    def from_coordinates(cls, x: int, y: int) -> IPoint:
        return cls.from_bytes(
            point_coord_to_bytes((x, y))
        )

    @staticmethod
    def curve_type() -> str:
        return "SLIP10-Ed25519"

    def underlying_object(self) -> Any:
        return self.m_enc_bytes

    def x(self) -> int:
        if self.m_x is None:
            self.m_x, self.m_y = point_bytes_to_coord(self.m_enc_bytes)
        return self.m_x

    def y(self) -> int:
        if self.m_y is None:
            self.m_x, self.m_y = point_bytes_to_coord(self.m_enc_bytes)
        return self.m_y

    def raw(self) -> bytes:
        return self.raw_decoded()

    def raw_encoded(self) -> bytes:
        return self.m_enc_bytes

    def raw_decoded(self) -> bytes:
        return int_encode(self.x()) + int_encode(self.y())

    def __add__(self, point: IPoint) -> IPoint:
        return self.__class__(
            point_add(self.m_enc_bytes, point.underlying_object())
        )

    def __radd__(self, point: IPoint) -> IPoint:
        return self + point

    def __mul__(self, scalar: int) -> IPoint:
        if self.m_is_generator:
            return self.__class__(
                point_scalar_mul_base(scalar)
            )
        return self.__class__(
            point_scalar_mul(scalar, self.m_enc_bytes)
        )

    def __rmul__(self, scalar: int) -> IPoint:
        return self * scalar


class SLIP10Ed25519PublicKey(IPublicKey):

    m_ver_key: signing.VerifyKey

    def __init__(self, key_obj: signing.VerifyKey) -> None:
        self.m_ver_key = key_obj

    @classmethod
    def from_bytes(cls, key_bytes: bytes) -> IPublicKey:
        # Remove the 0x00 prefix if present because nacl requires 32-byte length
        if (len(key_bytes) == PUBLIC_KEY_BYTE_LENGTH + len(PUBLIC_KEY_PREFIX)
                and key_bytes[0] == bytes_to_integer(PUBLIC_KEY_PREFIX)):
            key_bytes = key_bytes[1:]

        # nacl doesn't check if the point lies on curve
        if not point_is_on_curve(key_bytes):
            raise ValueError("Invalid public key bytes")

        try:
            return cls(signing.VerifyKey(key_bytes))
        except (exceptions.RuntimeError, exceptions.ValueError) as ex:
            raise ValueError("Invalid public key bytes") from ex

    @classmethod
    def from_point(cls, key_point: IPoint) -> IPublicKey:
        return cls.from_bytes(key_point.raw_encoded())

    @staticmethod
    def curve_type() -> str:
        return "SLIP10-Ed25519"

    @staticmethod
    def compressed_length() -> int:
        return PUBLIC_KEY_BYTE_LENGTH + len(PUBLIC_KEY_PREFIX)

    @staticmethod
    def uncompressed_length() -> int:
        return SLIP10Ed25519PublicKey.compressed_length()

    def underlying_object(self) -> Any:
        return self.m_ver_key

    def raw_compressed(self) -> bytes:
        return PUBLIC_KEY_PREFIX + bytes(self.m_ver_key)

    def raw_uncompressed(self) -> bytes:
        return self.raw_compressed()

    def point(self) -> IPoint:
        return SLIP10Ed25519Point(bytes(self.m_ver_key))


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
        return PRIVATE_KEY_BYTE_LENGTH

    def underlying_object(self) -> Any:
        return self.m_sign_key

    def raw(self) -> bytes:
        return bytes(self.m_sign_key)

    def public_key(self) -> IPublicKey:
        return SLIP10Ed25519PublicKey(self.m_sign_key.verify_key)


CURVE_ORDER: int = 2 ** 252 + 27742317777372353535851937790883648493
GENERATOR: IPoint = SLIP10Ed25519Point.from_coordinates(
    15112221349535400772501151409588531511454012693041857206046113283949847762202,
    46316835694926478169428394003475163141307993866256225615783033603165251855960
)

SLIP10Ed25519: EllipticCurveCryptography = EllipticCurveCryptography(
    "SLIP10-Ed25519", CURVE_ORDER, GENERATOR, SLIP10Ed25519Point, SLIP10Ed25519PublicKey, SLIP10Ed25519PrivateKey
)
