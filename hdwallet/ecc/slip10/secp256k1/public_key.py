#!/usr/bin/env python3

from typing import Any
from ecdsa.ecdsa import curve_secp256k1
from ecdsa import (
    curves, ellipticcurve, keys
)

import coincurve
import ecdsa

from ....const import SLIP10_SECP256K1_CONST
from ...iecc import (
    IPoint, IPublicKey
)
from .point import SLIP10Secp256k1Point


if SLIP10_SECP256K1_CONST.USE == "coincurve":

    class SLIP10Secp256k1PublicKey(IPublicKey):
        m_ver_key: coincurve.PublicKey = None

        def __init__(self, key_obj: coincurve.PublicKey) -> None:
            self.m_ver_key = key_obj

        @classmethod
        def from_bytes(cls, key_bytes: bytes) -> IPublicKey:
            try:
                return cls(coincurve.PublicKey(key_bytes))
            except ValueError as ex:
                raise ValueError("Invalid public key bytes") from ex

        @classmethod
        def from_point(cls, key_point: IPoint) -> IPublicKey:
            try:
                return cls(
                    coincurve.PublicKey.from_point(
                        key_point.x(), key_point.y()
                    )
                )
            except ValueError as ex:
                raise ValueError("Invalid public key point") from ex

        @staticmethod
        def curve_type() -> str:
            return "SLIP10-Secp256k1"

        @staticmethod
        def compressed_length() -> int:
            return SLIP10_SECP256K1_CONST.PUBLIC_KEY_COMPRESSED_BYTE_LENGTH

        @staticmethod
        def uncompressed_length() -> int:
            return SLIP10_SECP256K1_CONST.PUBLIC_KEY_UNCOMPRESSED_BYTE_LENGTH

        def underlying_object(self) -> Any:
            return self.m_ver_key

        def raw_compressed(self) -> bytes:
            return self.m_ver_key.format(True)

        def raw_uncompressed(self) -> bytes:
            return self.m_ver_key.format(False)

        def point(self) -> IPoint:
            point = self.m_ver_key.point()
            return SLIP10Secp256k1Point.from_coordinates(
                point[0], point[1]
            )

elif SLIP10_SECP256K1_CONST.USE == "ecdsa":

    class SLIP10Secp256k1PublicKey(IPublicKey):
        m_ver_key: ecdsa.VerifyingKey

        def __init__(self, key_obj: ecdsa.VerifyingKey) -> None:
            self.m_ver_key = key_obj

        @classmethod
        def from_bytes(cls, key_bytes: bytes) -> IPublicKey:
            try:
                return cls(
                    ecdsa.VerifyingKey.from_string(
                        key_bytes, curve=curves.SECP256k1
                    )
                )
            except keys.MalformedPointError as ex:
                raise ValueError("Invalid public key bytes") from ex

        @classmethod
        def from_point(cls, key_point: IPoint) -> IPublicKey:
            try:
                return cls(
                    ecdsa.VerifyingKey.from_public_point(
                        ellipticcurve.Point(
                            curve_secp256k1, key_point.x(), key_point.y()
                        ),
                        curve=curves.SECP256k1
                    )
                )
            except keys.MalformedPointError as ex:
                raise ValueError("Invalid public key point") from ex

        @staticmethod
        def curve_type() -> str:
            return "SLIP10-Secp256k1"

        @staticmethod
        def compressed_length() -> int:
            return SLIP10_SECP256K1_CONST.PUBLIC_KEY_COMPRESSED_BYTE_LENGTH

        @staticmethod
        def uncompressed_length() -> int:
            return SLIP10_SECP256K1_CONST.PUBLIC_KEY_UNCOMPRESSED_BYTE_LENGTH

        def underlying_object(self) -> Any:
            return self.m_ver_key

        def raw_compressed(self) -> bytes:
            return self.m_ver_key.to_string("compressed")

        def raw_uncompressed(self) -> bytes:
            return self.m_ver_key.to_string("uncompressed")

        def point(self) -> IPoint:
            return SLIP10Secp256k1Point(self.m_ver_key.pubkey.point)

else:
    Exception(
        f"Invalid SLIP10-Secp256k1 use, (expected: 'coincurve' or 'ecdsa', got: '{SLIP10_SECP256K1_CONST.USE}')"
    )
