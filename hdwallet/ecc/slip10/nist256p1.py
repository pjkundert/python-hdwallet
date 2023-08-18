#!/usr/bin/env python3

from typing import Any
from ecdsa.ecdsa import (
    curve_256, generator_256
)
from ecdsa import (
    curves, ellipticcurve, keys
)

import ecdsa

from .secp256k1 import (
    POINT_COORD_BYTE_LENGTH,
    PRIVATE_KEY_BYTE_LENGTH,
    PUBLIC_KEY_COMPRESSED_BYTE_LENGTH,
    PUBLIC_KEY_UNCOMPRESSED_BYTE_LENGTH
)
from ..ecc import (
    IPoint, IPublicKey, IPrivateKey, EllipticCurveCryptography
)
from ...utils import (
    bytes_to_integer, integer_to_bytes
)


class SLIP10Nist256p1Point(IPoint):

    m_point: ellipticcurve.PointJacobi

    def __init__(self, point_obj: ellipticcurve.PointJacobi) -> None:
        self.m_point = point_obj

    @classmethod
    def from_bytes(cls, point_bytes: bytes) -> IPoint:
        try:
            return cls(
                ellipticcurve.PointJacobi.from_bytes(
                    curve_256, point_bytes
                )
            )
        except keys.MalformedPointError as ex:
            raise ValueError("Invalid point key bytes") from ex
        # ECDSA < 0.17 doesn't have from_bytes method for PointJacobi
        except AttributeError:
            return cls.from_coordinates(
                bytes_to_integer(point_bytes[:POINT_COORD_BYTE_LENGTH]),
                bytes_to_integer(point_bytes[POINT_COORD_BYTE_LENGTH:])
            )

    @classmethod
    def from_coordinates(cls, x: int, y: int) -> IPoint:
        return cls(
            ellipticcurve.PointJacobi.from_affine(
                ellipticcurve.Point(curve_256, x, y)
            )
        )

    @staticmethod
    def curve_type() -> str:
        return "SLIP10-Nist256p1"

    def underlying_object(self) -> Any:
        return self.m_point

    def x(self) -> int:
        return self.m_point.x()

    def y(self) -> int:
        return self.m_point.y()

    def raw(self) -> bytes:
        return self.raw_decoded()

    def raw_encoded(self) -> bytes:
        try:
            return self.m_point.to_bytes("compressed")
        # ECDSA < 0.17 doesn't have to_bytes method for PointJacobi
        except AttributeError:
            x_bytes = integer_to_bytes(self.m_point.x(), POINT_COORD_BYTE_LENGTH)
            if self.m_point.y() & 1:
                enc_bytes = b"\x03" + x_bytes
            else:
                enc_bytes = b"\x02" + x_bytes
            return enc_bytes

    def raw_decoded(self) -> bytes:
        try:
            return self.m_point.to_bytes()
        # ECDSA < 0.17 doesn't have to_bytes method for PointJacobi
        except AttributeError:
            x_bytes = integer_to_bytes(self.m_point.x(), POINT_COORD_BYTE_LENGTH)
            y_bytes = integer_to_bytes(self.m_point.y(), POINT_COORD_BYTE_LENGTH)

            return x_bytes + y_bytes

    def __add__(self,
                point: IPoint) -> IPoint:
        return self.__class__(self.m_point + point.underlying_object())

    def __radd__(self,
                 point: IPoint) -> IPoint:
        return self + point

    def __mul__(self,
                scalar: int) -> IPoint:
        return self.__class__(self.m_point * scalar)

    def __rmul__(self,
                 scalar: int) -> IPoint:
        return self * scalar


class SLIP10Nist256p1PublicKey(IPublicKey):
    
    m_ver_key: ecdsa.VerifyingKey

    def __init__(self, key_obj: ecdsa.VerifyingKey) -> None:
        self.m_ver_key = key_obj

    @classmethod
    def from_bytes(cls, key_bytes: bytes) -> IPublicKey:
        try:
            return cls(
                ecdsa.VerifyingKey.from_string(
                    key_bytes, curve=curves.NIST256p
                )
            )
        except keys.MalformedPointError as ex:
            raise ValueError("Invalid public key bytes") from ex

    @classmethod
    def from_point(cls, key_point: IPoint) -> IPublicKey:
        try:
            return cls(
                ecdsa.VerifyingKey.from_public_point(
                    ellipticcurve.Point(
                        curve_256, key_point.x(), key_point.y()
                    ),
                    curve=curves.NIST256p
                )
            )
        except keys.MalformedPointError as ex:
            raise ValueError("Invalid public key point") from ex

    @staticmethod
    def curve_type() -> str:
        return "SLIP10-Nist256p1"

    @staticmethod
    def compressed_length() -> int:
        return PUBLIC_KEY_COMPRESSED_BYTE_LENGTH

    @staticmethod
    def uncompressed_length() -> int:
        return PUBLIC_KEY_UNCOMPRESSED_BYTE_LENGTH

    def underlying_object(self) -> Any:
        return self.m_ver_key

    def raw_compressed(self) -> bytes:
        return self.m_ver_key.to_string("compressed")

    def raw_uncompressed(self) -> bytes:
        return self.m_ver_key.to_string("uncompressed")

    def point(self) -> IPoint:
        return SLIP10Nist256p1Point(self.m_ver_key.pubkey.point)


class SLIP10Nist256p1PrivateKey(IPrivateKey):
    
    m_sign_key = ecdsa.SigningKey

    def __init__(self, key_obj: ecdsa.SigningKey) -> None:
        self.m_sign_key = key_obj

    @classmethod
    def from_bytes(cls, key_bytes: bytes) -> IPrivateKey:
        try:
            return cls(
                ecdsa.SigningKey.from_string(
                    key_bytes, curve=curves.NIST256p
                )
            )
        except keys.MalformedPointError as ex:
            raise ValueError("Invalid private key bytes") from ex

    @staticmethod
    def curve_type() -> str:
        return "SLIP10-Nist256p1"

    @staticmethod
    def length() -> int:
        return PRIVATE_KEY_BYTE_LENGTH

    def underlying_object(self) -> Any:
        return self.m_sign_key

    def raw(self) -> bytes:
        return self.m_sign_key.to_string()

    def public_key(self) -> IPublicKey:
        return SLIP10Nist256p1PublicKey(self.m_sign_key.get_verifying_key())


CURVE_ORDER: int = generator_256.order()
GENERATOR: IPoint = SLIP10Nist256p1Point(generator_256)

SLIP10Nist256p1: EllipticCurveCryptography = EllipticCurveCryptography(
    "SLIP10-Nist256p1", CURVE_ORDER, GENERATOR, SLIP10Nist256p1Point, SLIP10Nist256p1PublicKey, SLIP10Nist256p1PrivateKey
)
