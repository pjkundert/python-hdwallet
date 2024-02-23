#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from __future__ import annotations

from .ipoint import IPoint
from .ipublic_key import IPublicKey
from .iprivate_key import IPrivateKey


class IEllipticCurveCryptography:

    NAME: str
    ORDER: int
    GENERATOR: IPoint
    POINT: IPoint
    PUBLIC_KEY: IPublicKey
    PRIVATE_KEY: IPrivateKey
