#!/usr/bin/env python3

from __future__ import annotations

from abc import (
    ABC, abstractmethod
)
from typing import Any


class IPoint(ABC):

    @classmethod
    @abstractmethod
    def from_bytes(cls, point_bytes: bytes) -> IPoint:
        pass

    @classmethod
    @abstractmethod
    def from_coordinates(cls, x: int, y: int) -> IPoint:
        pass

    @staticmethod
    @abstractmethod
    def curve_type() -> str:
        pass

    @abstractmethod
    def underlying_object(self) -> Any:
        pass

    @abstractmethod
    def x(self) -> int:
        pass

    @abstractmethod
    def y(self) -> int:
        pass

    @abstractmethod
    def raw(self) -> bytes:
        pass

    @abstractmethod
    def raw_encoded(self) -> bytes:
        pass

    @abstractmethod
    def raw_decoded(self) -> bytes:
        pass

    @abstractmethod
    def __add__(self, point: IPoint) -> IPoint:
        pass

    @abstractmethod
    def __radd__(self, point: IPoint) -> IPoint:
        pass

    @abstractmethod
    def __mul__(self, scalar: int) -> IPoint:
        pass

    @abstractmethod
    def __rmul__(self, scalar: int) -> IPoint:
        pass


class IPublicKey(ABC):

    @classmethod
    @abstractmethod
    def from_bytes(cls, key_bytes: bytes) -> IPublicKey:
        pass

    @classmethod
    @abstractmethod
    def from_point(cls, key_point: IPoint) -> IPublicKey:
        pass

    @staticmethod
    @abstractmethod
    def curve_type() -> str:
        pass

    @classmethod
    def is_valid_bytes(cls, key_bytes: bytes) -> bool:
        try:
            cls.from_bytes(key_bytes)
            return True
        except ValueError:
            return False

    @classmethod
    def is_valid_point(cls, key_point: IPoint) -> bool:
        try:
            cls.from_point(key_point)
            return True
        except ValueError:
            return False

    @staticmethod
    @abstractmethod
    def compressed_length() -> int:
        pass

    @staticmethod
    @abstractmethod
    def uncompressed_length() -> int:
        pass

    @abstractmethod
    def underlying_object(self) -> Any:
        pass

    @abstractmethod
    def raw_compressed(self) -> bytes:
        pass

    @abstractmethod
    def raw_uncompressed(self) -> bytes:
        pass

    @abstractmethod
    def point(self) -> IPoint:
        pass


class IPrivateKey(ABC):

    @classmethod
    @abstractmethod
    def from_bytes(cls, key_bytes: bytes) -> IPrivateKey:
        pass

    @staticmethod
    @abstractmethod
    def curve_type() -> str:
        pass

    @classmethod
    def is_valid_bytes(cls, key_bytes: bytes) -> bool:
        try:
            cls.from_bytes(key_bytes)
            return True
        except ValueError:
            return False

    @staticmethod
    @abstractmethod
    def length() -> int:
        pass

    @abstractmethod
    def underlying_object(self) -> Any:
        pass

    @abstractmethod
    def raw(self) -> bytes:
        pass

    @abstractmethod
    def public_key(self) -> IPublicKey:
        pass


class EllipticCurveCryptography:

    m_curve_name: str
    m_order: int
    m_generator: Any
    m_point_cls: Any
    m_public_key_cls: Any
    m_private_key_cls: Any

    def __init__(
        self, curve_name: str, order: int, generator: Any, point_cls: Any, m_public_key_cls: Any, m_private_key_cls: Any
    ):
        self.m_curve_name = curve_name
        self.m_order = order
        self.m_generator = generator
        self.m_point_cls = point_cls
        self.m_public_key_cls = m_public_key_cls
        self.m_private_key_cls = m_private_key_cls

    def curve_name(self) -> str:
        return self.m_curve_name

    def order(self) -> int:
        return self.m_order

    def generator(self) -> IPoint:
        return self.m_generator

    def point_class(self) -> IPoint:
        return self.m_point_cls

    def public_key_class(self) -> IPublicKey:
        return self.m_public_key_cls

    def private_key_class(self) -> IPrivateKey:
        return self.m_private_key_cls
