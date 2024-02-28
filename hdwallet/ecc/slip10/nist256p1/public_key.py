#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Any
from ecdsa import VerifyingKey
from ecdsa.ecdsa import curve_256
from ecdsa import (
    curves, ellipticcurve, keys
)

from ....const import SLIP10_SECP256K1_CONST
from ...iecc import (
    IPoint, IPublicKey
)
from .point import SLIP10Nist256p1Point


class SLIP10Nist256p1PublicKey(IPublicKey):
    
    verify_key: VerifyingKey

    def __init__(self, verify_key: VerifyingKey) -> None:
        self.verify_key = verify_key

    @staticmethod
    def name() -> str:
        return "SLIP10-Nist256p1"

    @classmethod
    def from_bytes(cls, public_key: bytes) -> IPublicKey:
        try:
            return cls(
                VerifyingKey.from_string(
                    public_key, curve=curves.NIST256p
                )
            )
        except keys.MalformedPointError as ex:
            raise ValueError("Invalid public key bytes") from ex

    @classmethod
    def from_point(cls, point: IPoint) -> IPublicKey:
        try:
            return cls(
                VerifyingKey.from_public_point(
                    ellipticcurve.Point(
                        curve_256, point.x(), point.y()
                    ),
                    curve=curves.NIST256p
                )
            )
        except keys.MalformedPointError as ex:
            raise ValueError("Invalid public key point") from ex

    @staticmethod
    def compressed_length() -> int:
        return SLIP10_SECP256K1_CONST.PUBLIC_KEY_COMPRESSED_BYTE_LENGTH

    @staticmethod
    def uncompressed_length() -> int:
        return SLIP10_SECP256K1_CONST.PUBLIC_KEY_UNCOMPRESSED_BYTE_LENGTH

    def underlying_object(self) -> Any:
        return self.verify_key

    def raw_compressed(self) -> bytes:
        return self.verify_key.to_string("compressed")

    def raw_uncompressed(self) -> bytes:
        return self.verify_key.to_string("uncompressed")

    def point(self) -> IPoint:
        return SLIP10Nist256p1Point(self.verify_key.pubkey.point)
