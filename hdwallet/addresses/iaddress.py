#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from __future__ import annotations

from abc import (
    ABC, abstractmethod
)
from typing import (
    Union, Optional
)

from ..ecc import IPublicKey


class IAddress(ABC):

    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    @classmethod
    @abstractmethod
    def encode(cls, public_key: Union[bytes, IPublicKey], encode_type: Optional[str] = None, **kwargs) -> str:
        pass

    @classmethod
    @abstractmethod
    def decode(cls, address: str, decode_type: Optional[str] = None, **kwargs) -> str:
        pass
