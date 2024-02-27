#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Any
from nacl.signing import VerifyKey
from nacl import exceptions

from ....const import SLIP10_ED25519_CONST
from ....libs.ed25519 import point_is_on_curve
from ....utils import bytes_to_integer
from ...iecc import (
    IPoint, IPublicKey
)
from .point import SLIP10Ed25519Point


class SLIP10Ed25519PublicKey(IPublicKey):

    verify_key: VerifyKey

    def __init__(self, verify_key: VerifyKey) -> None:
        self.verify_key = verify_key

    @staticmethod
    def name() -> str:
        return "SLIP10-Ed25519"

    @classmethod
    def from_bytes(cls, public_key: bytes) -> IPublicKey:
        if (len(public_key) == SLIP10_ED25519_CONST.PUBLIC_KEY_BYTE_LENGTH + len(SLIP10_ED25519_CONST.PUBLIC_KEY_PREFIX)
                and public_key[0] == bytes_to_integer(SLIP10_ED25519_CONST.PUBLIC_KEY_PREFIX)):
            public_key = public_key[1:]

        if not point_is_on_curve(public_key):
            raise ValueError("Invalid public key bytes")

        try:
            return cls(VerifyKey(public_key))
        except (exceptions.RuntimeError, exceptions.ValueError) as ex:
            raise ValueError("Invalid public key bytes") from ex

    @classmethod
    def from_point(cls, point: IPoint) -> IPublicKey:
        return cls.from_bytes(point.raw_encoded())

    @staticmethod
    def compressed_length() -> int:
        return SLIP10_ED25519_CONST.PUBLIC_KEY_BYTE_LENGTH + len(SLIP10_ED25519_CONST.PUBLIC_KEY_PREFIX)

    @staticmethod
    def uncompressed_length() -> int:
        return SLIP10Ed25519PublicKey.compressed_length()

    def underlying_object(self) -> Any:
        return self.verify_key

    def raw_compressed(self) -> bytes:
        return SLIP10_ED25519_CONST.PUBLIC_KEY_PREFIX + bytes(self.verify_key)

    def raw_uncompressed(self) -> bytes:
        return self.raw_compressed()

    def point(self) -> IPoint:
        return SLIP10Ed25519Point(bytes(self.verify_key))
