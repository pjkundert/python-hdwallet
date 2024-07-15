#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from __future__ import annotations

from typing import Any
from abc import (
    ABC, abstractmethod
)

from .ipoint import IPoint


class IPublicKey(ABC):

    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    @classmethod
    @abstractmethod
    def from_bytes(cls, public_key: bytes) -> "IPublicKey":
        pass

    @classmethod
    @abstractmethod
    def from_point(cls, point: IPoint) -> "IPublicKey":
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

    @abstractmethod
    def underlying_object(self) -> Any:
        pass

    @staticmethod
    @abstractmethod
    def compressed_length() -> int:
        pass

    @staticmethod
    @abstractmethod
    def uncompressed_length() -> int:
        pass

    @classmethod
    def is_valid_bytes(cls, public_key: bytes) -> bool:
        """
        Checks if the given bytes represent a valid bytes.

        :param public_key: The byte array to be validated.
        :type public_key: bytes

        :return: True if the byte array represents a valid public key, False otherwise.
        :rtype: bool
        """

        try:
            cls.from_bytes(public_key)
            return True
        except ValueError:
            return False

    @classmethod
    def is_valid_point(cls, point: IPoint) -> bool:
        """
        Checks if the given point is a valid point.

        :param point: The point to be validated.
        :type point: IPoint

        :return: True if the point is valid, False otherwise.
        :rtype: bool
        """

        try:
            cls.from_point(point)
            return True
        except ValueError:
            return False
