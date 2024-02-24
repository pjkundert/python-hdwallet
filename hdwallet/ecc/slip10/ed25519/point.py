#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Optional, Any
)

from ....libs.ed25519 import (
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
from ...iecc import IPoint


class SLIP10Ed25519Point(IPoint):

    is_generator: bool
    point: bytes
    _x: Optional[int]
    _y: Optional[int]

    def __init__(self, point: bytes) -> None:
        if not point_is_encoded_bytes(point):
            raise ValueError("Invalid point bytes")

        self.point = point
        self.is_generator = point_is_generator(point)
        self._x, self._y = None, None

    @staticmethod
    def name() -> str:
        return "SLIP10-Ed25519"

    @classmethod
    def from_bytes(cls, point: bytes) -> IPoint:
        if not point_is_on_curve(point):
            raise ValueError("Invalid point bytes")
        if point_is_decoded_bytes(point):
            point = point_encode(
                point_bytes_to_coord(point)
            )
        return cls(point)

    @classmethod
    def from_coordinates(cls, x: int, y: int) -> IPoint:
        return cls.from_bytes(
            point_coord_to_bytes((x, y))
        )

    def underlying_object(self) -> Any:
        return self.point

    def x(self) -> int:
        if self._x is None:
            self._x, self._y = point_bytes_to_coord(self.point)
        return self._x

    def y(self) -> int:
        if self._y is None:
            self._x, self._y = point_bytes_to_coord(self.point)
        return self._y

    def raw(self) -> bytes:
        return self.raw_decoded()

    def raw_encoded(self) -> bytes:
        return self.point

    def raw_decoded(self) -> bytes:
        return int_encode(self.x()) + int_encode(self.y())

    def __add__(self, point: IPoint) -> IPoint:
        return self.__class__(
            point_add(self.point, point.underlying_object())
        )

    def __radd__(self, point: IPoint) -> IPoint:
        return self + point

    def __mul__(self, scalar: int) -> IPoint:
        if self.is_generator:
            return self.__class__(
                point_scalar_mul_base(scalar)
            )
        return self.__class__(
            point_scalar_mul(scalar, self.point)
        )

    def __rmul__(self, scalar: int) -> IPoint:
        return self * scalar
