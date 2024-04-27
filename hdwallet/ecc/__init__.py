#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Dict, List, Type, Union
)

from ..exceptions import ECCError
from ..utils import get_bytes
from .kholaw import (
    KholawEd25519ECC, KholawEd25519Point, KholawEd25519PublicKey, KholawEd25519PrivateKey
)
from .slip10 import (
    SLIP10Ed25519ECC, SLIP10Ed25519Point, SLIP10Ed25519PublicKey, SLIP10Ed25519PrivateKey,
    SLIP10Ed25519Blake2bECC, SLIP10Ed25519Blake2bPoint, SLIP10Ed25519Blake2bPublicKey, SLIP10Ed25519Blake2bPrivateKey,
    SLIP10Ed25519MoneroECC, SLIP10Ed25519MoneroPoint, SLIP10Ed25519MoneroPublicKey, SLIP10Ed25519MoneroPrivateKey,
    SLIP10Nist256p1ECC, SLIP10Nist256p1Point, SLIP10Nist256p1PublicKey, SLIP10Nist256p1PrivateKey,
    SLIP10Secp256k1ECC, SLIP10Secp256k1Point, SLIP10Secp256k1PublicKey, SLIP10Secp256k1PrivateKey
)
from .iecc import (
    IPoint, IPublicKey, IPrivateKey, IEllipticCurveCryptography
)


class ECCS:

    dictionary: Dict[str, Type[IEllipticCurveCryptography]] = {
        KholawEd25519ECC.NAME: KholawEd25519ECC,
        SLIP10Ed25519ECC.NAME: SLIP10Ed25519ECC,
        SLIP10Ed25519Blake2bECC.NAME: SLIP10Ed25519Blake2bECC,
        SLIP10Ed25519MoneroECC.NAME: SLIP10Ed25519MoneroECC,
        SLIP10Nist256p1ECC.NAME: SLIP10Nist256p1ECC,
        SLIP10Secp256k1ECC.NAME: SLIP10Secp256k1ECC
    }

    @classmethod
    def names(cls) -> List[str]:
        return list(cls.dictionary.keys())

    @classmethod
    def classes(cls) -> List[Type[IEllipticCurveCryptography]]:
        return list(cls.dictionary.values())

    @classmethod
    def ecc(cls, name: str) -> Type[IEllipticCurveCryptography]:

        if not cls.is_ecc(name=name):
            raise ECCError(
                "Invalid ECC name", expected=cls.names(), got=name
            )

        return cls.dictionary[name]

    @classmethod
    def is_ecc(cls, name: str) -> bool:
        return name in cls.names()


def validate_and_get_public_key(
    public_key: Union[bytes, str, IPublicKey], public_key_cls: Type[IPublicKey]
) -> IPublicKey:
    if isinstance(public_key, bytes):
        public_key: IPublicKey = public_key_cls.from_bytes(public_key)
    elif isinstance(public_key, str):
        public_key: IPublicKey = public_key_cls.from_bytes(get_bytes(public_key))
    elif not isinstance(public_key, public_key_cls):
        ecc: Type[IEllipticCurveCryptography] = ECCS.ecc(
            name=public_key_cls.name()
        )
        raise TypeError(
            f"A {ecc.NAME} public key is required, (expected: {public_key_cls}, got: {type(public_key)}"
        )
    return public_key


__all__: List[str] = [
    "IPoint", "IPublicKey", "IPrivateKey", "IEllipticCurveCryptography",
    "KholawEd25519Point", "KholawEd25519PublicKey", "KholawEd25519PrivateKey",
    "SLIP10Ed25519Point", "SLIP10Ed25519PublicKey", "SLIP10Ed25519PrivateKey",
    "SLIP10Ed25519Blake2bPoint", "SLIP10Ed25519Blake2bPublicKey", "SLIP10Ed25519Blake2bPrivateKey",
    "SLIP10Ed25519MoneroPoint", "SLIP10Ed25519MoneroPublicKey", "SLIP10Ed25519MoneroPrivateKey",
    "SLIP10Nist256p1Point", "SLIP10Nist256p1PublicKey", "SLIP10Nist256p1PrivateKey",
    "SLIP10Secp256k1Point", "SLIP10Secp256k1PublicKey", "SLIP10Secp256k1PrivateKey",
    "ECCS", "validate_and_get_public_key"
] + [
    cls.__name__ for cls in ECCS.classes()
]
