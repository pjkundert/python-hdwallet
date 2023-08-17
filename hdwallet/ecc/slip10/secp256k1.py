#!/usr/bin/env python3

from typing import Any
from ecdsa.ecdsa import (
    curve_secp256k1, generator_secp256k1
)
from ecdsa import (
    curves, ellipticcurve, keys
)

import coincurve
import ecdsa

from ..ecc import (
    IPoint, IPublicKey, IPrivateKey, EllipticCurveCryptography
)
from ...utils import (
    bytes_to_integer, integer_to_bytes
)

USE_COINCURVE: bool = False
# Point coordinate length in bytes
POINT_COORD_BYTE_LENGTH: int = 32
# Private key length in bytes
PRIVATE_KEY_BYTE_LENGTH: int = 32
# Uncompressed public key prefix
PUBLIC_KEY_UNCOMPRESSED_PREFIX: bytes = b"\x04"
# Compressed public key length in bytes
PUBLIC_KEY_COMPRESSED_BYTE_LENGTH: int = 33
# Uncompressed public key length in bytes
PUBLIC_KEY_UNCOMPRESSED_BYTE_LENGTH: int = 65


class SLIP10Secp256k1PointCoinCurve(IPoint):

    m_pub_key: coincurve.PublicKey

    def __init__(self, point_obj: coincurve.PublicKey) -> None:
        self.m_pub_key = point_obj

    @classmethod
    def from_bytes(cls, point_bytes: bytes) -> IPoint:
        if len(point_bytes) == PUBLIC_KEY_UNCOMPRESSED_BYTE_LENGTH - 1:
            return cls(coincurve.PublicKey(PUBLIC_KEY_UNCOMPRESSED_PREFIX + point_bytes))
        if len(point_bytes) == PUBLIC_KEY_COMPRESSED_BYTE_LENGTH:
            return cls(coincurve.PublicKey(point_bytes))
        raise ValueError("Invalid point bytes")

    @classmethod
    def from_coordinates(cls, x: int, y: int) -> IPoint:
        try:
            return cls(coincurve.PublicKey.from_point(x, y))
        except ValueError as ex:
            raise ValueError("Invalid point coordinates") from ex

    @staticmethod
    def curve_type() -> str:
        return "SLIP10-Secp256k1"

    def underlying_object(self) -> Any:
        return self.m_pub_key

    def x(self) -> int:
        return self.m_pub_key.point()[0]

    def y(self) -> int:
        return self.m_pub_key.point()[1]

    def raw(self) -> bytes:
        return self.raw_decoded()

    def raw_encoded(self) -> bytes:
        return self.m_pub_key.format(True)

    def raw_decoded(self) -> bytes:
        return self.m_pub_key.format(False)[1:]

    def __add__(self, point: IPoint) -> IPoint:
        return self.__class__(self.m_pub_key.combine([point.underlying_object()]))

    def __radd__(self, point: IPoint) -> IPoint:
        return self + point

    def __mul__(self, scalar: int) -> IPoint:
        bytes_num = None or ((scalar.bit_length() if scalar > 0 else 1) + 7) // 8
        return self.__class__(self.m_pub_key.multiply(scalar.to_bytes(bytes_num, byteorder="big", signed=False)))

    def __rmul__(self, scalar: int) -> IPoint:
        return self * scalar


class SLIP10Secp256k1PublicKeyCoinCurve(IPublicKey):

    m_ver_key: coincurve.PublicKey = None

    def __init__(self, key_obj: coincurve.PublicKey) -> None:
        self.m_ver_key = key_obj

    @classmethod
    def from_bytes(cls, key_bytes: bytes) -> IPublicKey:
        try:
            return cls(coincurve.PublicKey(key_bytes))
        except ValueError as ex:
            raise ValueError("Invalid public key bytes") from ex

    @classmethod
    def from_point(cls, key_point: IPoint) -> IPublicKey:
        try:
            return cls(
                coincurve.PublicKey.from_point(
                    key_point.x(), key_point.y()
                )
            )
        except ValueError as ex:
            raise ValueError("Invalid public key point") from ex

    @staticmethod
    def curve_type() -> str:
        return "SLIP10-Secp256k1"

    @staticmethod
    def compressed_length() -> int:
        return PUBLIC_KEY_COMPRESSED_BYTE_LENGTH

    @staticmethod
    def uncompressed_length() -> int:
        return PUBLIC_KEY_UNCOMPRESSED_BYTE_LENGTH

    def underlying_object(self) -> Any:
        return self.m_ver_key

    def raw_compressed(self) -> bytes:
        return self.m_ver_key.format(True)

    def raw_uncompressed(self) -> bytes:
        return self.m_ver_key.format(False)

    def point(self) -> IPoint:
        point = self.m_ver_key.point()
        return SLIP10Secp256k1PointCoinCurve.from_coordinates(
            point[0], point[1]
        )


class SLIP10Secp256k1PrivateKeyCoinCurve(IPrivateKey):

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
        return PRIVATE_KEY_BYTE_LENGTH

    def underlying_object(self) -> Any:
        return self.m_sign_key

    def raw(self) -> bytes:
        return self.m_sign_key.secret

    def public_key(self) -> IPublicKey:
        return SLIP10Secp256k1PublicKeyCoinCurve(self.m_sign_key.public_key)


class SLIP10Secp256k1PointECDSA(IPoint):

    m_point: ellipticcurve.PointJacobi
    
    def __init__(self, point_obj: ellipticcurve.PointJacobi) -> None:
        self.m_point = point_obj

    @classmethod
    def from_bytes(cls, point_bytes: bytes) -> IPoint:
        try:
            return cls(
                ellipticcurve.PointJacobi.from_bytes(
                    curve_secp256k1, point_bytes
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
                ellipticcurve.Point(curve_secp256k1, x, y)
            )
        )

    @staticmethod
    def curve_type() -> str:
        return "SLIP10-Secp256k1"

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


class SLIP10Secp256k1PublicKeyECDSA(IPublicKey):

    m_ver_key: ecdsa.VerifyingKey

    def __init__(self, key_obj: ecdsa.VerifyingKey) -> None:
        self.m_ver_key = key_obj

    @classmethod
    def from_bytes(cls, key_bytes: bytes) -> IPublicKey:
        try:
            return cls(
                ecdsa.VerifyingKey.from_string(
                    key_bytes, curve=curves.SECP256k1
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
                        curve_secp256k1, key_point.x(), key_point.y()
                    ),
                    curve=curves.SECP256k1
                )
            )
        except keys.MalformedPointError as ex:
            raise ValueError("Invalid public key point") from ex

    @staticmethod
    def curve_type() -> str:
        return "SLIP10-Secp256k1"

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
        return SLIP10Secp256k1PointECDSA(self.m_ver_key.pubkey.point)


class SLIP10Secp256k1PrivateKeyECDSA(IPrivateKey):

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
        return PRIVATE_KEY_BYTE_LENGTH

    def underlying_object(self) -> Any:
        return self.m_sign_key

    def raw(self) -> bytes:
        return self.m_sign_key.to_string()

    def public_key(self) -> IPublicKey:
        return SLIP10Secp256k1PublicKeyECDSA(self.m_sign_key.get_verifying_key())


if USE_COINCURVE:
    SLIP10Secp256k1Point = SLIP10Secp256k1PointCoinCurve
    SLIP10Secp256k1PublicKey = SLIP10Secp256k1PublicKeyCoinCurve
    SLIP10Secp256k1PrivateKey = SLIP10Secp256k1PrivateKeyCoinCurve
    CURVE_ORDER: int = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    GENERATOR: IPoint = SLIP10Secp256k1Point.from_coordinates(
        0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
        0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
    )
else:
    SLIP10Secp256k1Point = SLIP10Secp256k1PointECDSA
    SLIP10Secp256k1PublicKey = SLIP10Secp256k1PublicKeyECDSA
    SLIP10Secp256k1PrivateKey = SLIP10Secp256k1PrivateKeyECDSA
    CURVE_ORDER: int = generator_secp256k1.order()
    GENERATOR: IPoint = SLIP10Secp256k1Point(generator_secp256k1)

SLIP10Secp256k1: EllipticCurveCryptography = EllipticCurveCryptography(
    "SLIP10-Secp256k1", CURVE_ORDER, GENERATOR, SLIP10Secp256k1Point, SLIP10Secp256k1PublicKey, SLIP10Secp256k1PrivateKey
)
