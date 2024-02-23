#!/usr/bin/env python3

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
