#!/usr/bin/env python3

from typing import Any
from ecdsa import VerifyingKey
from ecdsa.ecdsa import curve_secp256k1
from ecdsa import (
    curves, ellipticcurve, keys
)

from ....const import SLIP10_SECP256K1_CONST
from ...iecc import (
    IPoint, IPublicKey
)
from .point import SLIP10Secp256k1Point


if SLIP10_SECP256K1_CONST.USE == "coincurve":

    import coincurve

    class SLIP10Secp256k1PublicKey(IPublicKey):

        verify_key: coincurve.PublicKey

        def __init__(self, public_key: coincurve.PublicKey) -> None:
            self.verify_key = public_key

        @staticmethod
        def name() -> str:
            return "SLIP10-Secp256k1"

        @classmethod
        def from_bytes(cls, public_key: bytes) -> IPublicKey:
            try:
                return cls(coincurve.PublicKey(public_key))
            except ValueError as ex:
                raise ValueError("Invalid public key bytes") from ex

        @classmethod
        def from_point(cls, point: IPoint) -> IPublicKey:
            try:
                return cls(
                    coincurve.PublicKey.from_point(
                        point.x(), point.y()
                    )
                )
            except ValueError as ex:
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
            return self.verify_key.format(True)

        def raw_uncompressed(self) -> bytes:
            return self.verify_key.format(False)

        def point(self) -> IPoint:
            point = self.verify_key.point()
            return SLIP10Secp256k1Point.from_coordinates(
                point[0], point[1]
            )

elif SLIP10_SECP256K1_CONST.USE == "ecdsa":

    class SLIP10Secp256k1PublicKey(IPublicKey):

        verify_key: VerifyingKey

        def __init__(self, verify_key: VerifyingKey) -> None:
            self.verify_key = verify_key

        @staticmethod
        def name() -> str:
            return "SLIP10-Secp256k1"

        @classmethod
        def from_bytes(cls, public_key: bytes) -> IPublicKey:
            try:
                return cls(
                    VerifyingKey.from_string(
                        public_key, curve=curves.SECP256k1
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
                            curve_secp256k1, point.x(), point.y()
                        ),
                        curve=curves.SECP256k1
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
            return SLIP10Secp256k1Point(self.verify_key.pubkey.point)

else:
    Exception(
        f"Invalid SLIP10-Secp256k1 use, (expected: 'coincurve' or 'ecdsa', got: '{SLIP10_SECP256K1_CONST.USE}')"
    )
