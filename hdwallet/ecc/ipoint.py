#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from __future__ import annotations

from typing import Any
from abc import (
    ABC, abstractmethod
)


class IPoint(ABC):

    @classmethod
    @abstractmethod
    def from_bytes(cls, point_bytes: bytes) -> 'IPoint':
        pass

    @classmethod
    @abstractmethod
    def from_coordinates(cls, x: int, y: int) -> 'IPoint':
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
    def underlying_object(self) -> Any:
        pass

    @staticmethod
    @abstractmethod
    def curve_type() -> str:
        pass

    @abstractmethod
    def __add__(self, point: 'IPoint') -> 'IPoint':
        pass

    @abstractmethod
    def __radd__(self, point: 'IPoint') -> 'IPoint':
        pass

    @abstractmethod
    def __mul__(self, scalar: int) -> 'IPoint':
        pass

    @abstractmethod
    def __rmul__(self, scalar: int) -> 'IPoint':
        pass
