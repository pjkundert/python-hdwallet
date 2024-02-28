#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Any
from ecdsa.ecdsa import curve_256
from ecdsa.ellipticcurve import (
    Point, PointJacobi
)
from ecdsa import keys

from ....const import SLIP10_SECP256K1_CONST
from ...iecc import IPoint
from ....utils import (
    bytes_to_integer, integer_to_bytes
)


class SLIP10Nist256p1Point(IPoint):

    point: PointJacobi

    def __init__(self, point: PointJacobi) -> None:
        self.point = point

    @staticmethod
    def name() -> str:
        return "SLIP10-Nist256p1"

    @classmethod
    def from_bytes(cls, point: bytes) -> "SLIP10Nist256p1Point":
        try:
            return cls(
                PointJacobi.from_bytes(
                    curve_256, point
                )
            )
        except keys.MalformedPointError as ex:
            raise ValueError("Invalid point key bytes") from ex
        except AttributeError:
            return cls.from_coordinates(
                bytes_to_integer(point[:SLIP10_SECP256K1_CONST.POINT_COORDINATE_BYTE_LENGTH]),
                bytes_to_integer(point[SLIP10_SECP256K1_CONST.POINT_COORDINATE_BYTE_LENGTH:])
            )

    @classmethod
    def from_coordinates(cls, x: int, y: int) -> "SLIP10Nist256p1Point":
        return cls(
            PointJacobi.from_affine(
                Point(curve_256, x, y)
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
            x_bytes = integer_to_bytes(self.point.x(), SLIP10_SECP256K1_CONST.POINT_COORDINATE_BYTE_LENGTH)
            if self.point.y() & 1:
                enc_bytes = b"\x03" + x_bytes
            else:
                enc_bytes = b"\x02" + x_bytes
            return enc_bytes

    def raw_decoded(self) -> bytes:
        try:
            return self.point.to_bytes()
        except AttributeError:
            x_bytes = integer_to_bytes(self.point.x(), SLIP10_SECP256K1_CONST.POINT_COORDINATE_BYTE_LENGTH)
            y_bytes = integer_to_bytes(self.point.y(), SLIP10_SECP256K1_CONST.POINT_COORDINATE_BYTE_LENGTH)

            return x_bytes + y_bytes

    def __add__(self, point: IPoint) -> IPoint:
        return self.__class__(self.point + point.underlying_object())

    def __radd__(self, point: IPoint) -> IPoint:
        return self + point

    def __mul__(self, scalar: int) -> IPoint:
        return self.__class__(self.point * scalar)

    def __rmul__(self, scalar: int) -> IPoint:
        return self * scalar
