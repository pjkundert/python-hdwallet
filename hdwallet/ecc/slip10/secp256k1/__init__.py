#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from ecdsa.ecdsa import generator_secp256k1

from ....const import SLIP10_SECP256K1_CONST
from ...iecc import IEllipticCurveCryptography
from .point import SLIP10Secp256k1Point
from .public_key import SLIP10Secp256k1PublicKey
from .private_key import SLIP10Secp256k1PrivateKey


class SLIP10Secp256k1(IEllipticCurveCryptography):

    NAME = "SLIP10-Secp256k1"
    if SLIP10_SECP256K1_CONST.USE == "coincurve":
        ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        GENERATOR = SLIP10Secp256k1Point.from_coordinates(
            0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
            0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        )
    elif SLIP10_SECP256K1_CONST.USE == "ecdsa":
        ORDER = generator_secp256k1.order()
        GENERATOR = SLIP10Secp256k1Point(generator_secp256k1)
    else:
        Exception(
            f"Invalid SLIP10-Secp256k1 use, (expected: 'coincurve' or 'ecdsa', got: '{SLIP10_SECP256K1_CONST.USE}')"
        )
    POINT = SLIP10Secp256k1Point
    PUBLIC_KEY = SLIP10Secp256k1PublicKey
    PRIVATE_KEY = SLIP10Secp256k1PrivateKey
