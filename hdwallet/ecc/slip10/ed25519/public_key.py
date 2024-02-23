#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Any
from nacl import (
    exceptions, signing
)

from ....const import SLIP10_ED25519_CONST
from ....libs.ed25519 import point_is_on_curve
from ....utils import bytes_to_integer
from ...iecc import (
    IPoint, IPublicKey
)
from .point import SLIP10Ed25519Point


class SLIP10Ed25519PublicKey(IPublicKey):

    m_ver_key: signing.VerifyKey

    def __init__(self, key_obj: signing.VerifyKey) -> None:
        self.m_ver_key = key_obj

    @classmethod
    def from_bytes(cls, key_bytes: bytes) -> IPublicKey:
        # Remove the 0x00 prefix if present because nacl requires 32-byte length
        if (len(key_bytes) == SLIP10_ED25519_CONST.PUBLIC_KEY_BYTE_LENGTH + len(SLIP10_ED25519_CONST.PUBLIC_KEY_PREFIX)
                and key_bytes[0] == bytes_to_integer(SLIP10_ED25519_CONST.PUBLIC_KEY_PREFIX)):
            key_bytes = key_bytes[1:]

        # nacl doesn't check if the point lies on curve
        if not point_is_on_curve(key_bytes):
            raise ValueError("Invalid public key bytes")

        try:
            return cls(signing.VerifyKey(key_bytes))
        except (exceptions.RuntimeError, exceptions.ValueError) as ex:
            raise ValueError("Invalid public key bytes") from ex

    @classmethod
    def from_point(cls, key_point: IPoint) -> IPublicKey:
        return cls.from_bytes(key_point.raw_encoded())

    @staticmethod
    def curve_type() -> str:
        return "SLIP10-Ed25519"

    @staticmethod
    def compressed_length() -> int:
        return SLIP10_ED25519_CONST.PUBLIC_KEY_BYTE_LENGTH + len(SLIP10_ED25519_CONST.PUBLIC_KEY_PREFIX)

    @staticmethod
    def uncompressed_length() -> int:
        return SLIP10Ed25519PublicKey.compressed_length()

    def underlying_object(self) -> Any:
        return self.m_ver_key

    def raw_compressed(self) -> bytes:
        return SLIP10_ED25519_CONST.PUBLIC_KEY_PREFIX + bytes(self.m_ver_key)

    def raw_uncompressed(self) -> bytes:
        return self.raw_compressed()

    def point(self) -> IPoint:
        return SLIP10Ed25519Point(bytes(self.m_ver_key))
