#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Any
from ecdsa.ecdsa import curve_secp256k1
from ecdsa.ellipticcurve import (
    Point, PointJacobi
)
from ecdsa import keys

from ....const import SLIP10_SECP256K1_CONST
from ...iecc import IPoint
from ....utils import (
    bytes_to_integer, integer_to_bytes
)


if SLIP10_SECP256K1_CONST.USE == "coincurve":

    import coincurve

    class SLIP10Secp256k1Point(IPoint):

        public_key: coincurve.PublicKey

        def __init__(self, public_key: coincurve.PublicKey) -> None:
            self.public_key = public_key

        @staticmethod
        def name() -> str:
            return "SLIP10-Secp256k1"

        @classmethod
        def from_bytes(cls, point_bytes: bytes) -> IPoint:
            if len(point_bytes) == SLIP10_SECP256K1_CONST.PUBLIC_KEY_UNCOMPRESSED_BYTE_LENGTH - 1:
                return cls(coincurve.PublicKey(SLIP10_SECP256K1_CONST.PUBLIC_KEY_UNCOMPRESSED_PREFIX + point_bytes))
            if len(point_bytes) == SLIP10_SECP256K1_CONST.PUBLIC_KEY_COMPRESSED_BYTE_LENGTH:
                return cls(coincurve.PublicKey(point_bytes))
            raise ValueError("Invalid point bytes")

        @classmethod
        def from_coordinates(cls, x: int, y: int) -> IPoint:
            try:
                return cls(coincurve.PublicKey.from_point(x, y))
            except ValueError as ex:
                raise ValueError("Invalid point coordinates") from ex

        def underlying_object(self) -> Any:
            return self.public_key

        def x(self) -> int:
            return self.public_key.point()[0]

        def y(self) -> int:
            return self.public_key.point()[1]

        def raw(self) -> bytes:
            return self.raw_decoded()

        def raw_encoded(self) -> bytes:
            return self.public_key.format(True)

        def raw_decoded(self) -> bytes:
            return self.public_key.format(False)[1:]

        def __add__(self, point: IPoint) -> IPoint:
            return self.__class__(self.public_key.combine([point.underlying_object()]))

        def __radd__(self, point: IPoint) -> IPoint:
            return self + point

        def __mul__(self, scalar: int) -> IPoint:
            bytes_num = None or ((scalar.bit_length() if scalar > 0 else 1) + 7) // 8
            return self.__class__(self.public_key.multiply(scalar.to_bytes(bytes_num, byteorder="big", signed=False)))

        def __rmul__(self, scalar: int) -> IPoint:
            return self * scalar

elif SLIP10_SECP256K1_CONST.USE == "ecdsa":

    class SLIP10Secp256k1Point(IPoint):

        point: PointJacobi

        def __init__(self, point_obj: PointJacobi) -> None:
            self.point = point_obj

        @staticmethod
        def name() -> str:
            return "SLIP10-Secp256k1"

        @classmethod
        def from_bytes(cls, point_bytes: bytes) -> IPoint:
            try:
                return cls(
                    PointJacobi.from_bytes(
                        curve_secp256k1, point_bytes
                    )
                )
            except keys.MalformedPointError as ex:
                raise ValueError("Invalid point key bytes") from ex
            except AttributeError:
                return cls.from_coordinates(
                    bytes_to_integer(point_bytes[:SLIP10_SECP256K1_CONST.POINT_COORDINATE_BYTE_LENGTH]),
                    bytes_to_integer(point_bytes[SLIP10_SECP256K1_CONST.POINT_COORDINATE_BYTE_LENGTH:])
                )

        @classmethod
        def from_coordinates(cls, x: int, y: int) -> IPoint:
            return cls(
                PointJacobi.from_affine(
                    Point(curve_secp256k1, x, y)
                )
            )

        def underlying_object(self) -> Any:
            return self.point

        def x(self) -> int:
            return self.point.x()

        def y(self) -> int:
            return self.point.y()

        def raw(self) -> bytes:
            return self.raw_decoded()

        def raw_encoded(self) -> bytes:
            try:
                return self.point.to_bytes("compressed")
            except AttributeError:
                x: bytes = integer_to_bytes(self.point.x(), SLIP10_SECP256K1_CONST.POINT_COORDINATE_BYTE_LENGTH)
                return b"\x03" + x if self.point.y() & 1 else b"\x02" + x

        def raw_decoded(self) -> bytes:
            try:
                return self.point.to_bytes()
            except AttributeError:
                x: bytes = integer_to_bytes(self.point.x(), SLIP10_SECP256K1_CONST.POINT_COORDINATE_BYTE_LENGTH)
                y: bytes = integer_to_bytes(self.point.y(), SLIP10_SECP256K1_CONST.POINT_COORDINATE_BYTE_LENGTH)

                return x + y

        def __add__(self, point: IPoint) -> IPoint:
            return self.__class__(self.point + point.underlying_object())

        def __radd__(self, point: IPoint) -> IPoint:
            return self + point

        def __mul__(self, scalar: int) -> IPoint:
            return self.__class__(self.point * scalar)

        def __rmul__(self, scalar: int) -> IPoint:
            return self * scalar

else:
    Exception(
        f"Invalid SLIP10-Secp256k1 use, (expected: 'coincurve' or 'ecdsa', got: '{SLIP10_SECP256K1_CONST.USE}')"
    )
