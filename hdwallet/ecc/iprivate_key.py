#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from __future__ import annotations

from typing import Any
from abc import (
    ABC, abstractmethod
)

from .ipublic_key import IPublicKey


class IPrivateKey(ABC):

    @classmethod
    @abstractmethod
    def from_bytes(cls, key_bytes: bytes) -> 'IPrivateKey':
        pass

    @abstractmethod
    def raw(self) -> bytes:
        pass

    @abstractmethod
    def public_key(self) -> IPublicKey:
        pass

    @abstractmethod
    def underlying_object(self) -> Any:
        pass

    @staticmethod
    @abstractmethod
    def curve_type() -> str:
        pass

    @staticmethod
    @abstractmethod
    def length() -> int:
        pass

    @classmethod
    def is_valid_bytes(cls, key_bytes: bytes) -> bool:
        try:
            cls.from_bytes(key_bytes)
            return True
        except ValueError:
            return False
