#!/usr/bin/env python3

from abc import (
    ABC, abstractmethod
)
from binascii import unhexlify
from typing import (
    Any, Union, Type, Dict
)

from ..ecc import (
    EllipticCurveCryptography,
    ECC_TYPE_TO_INSTANCE,
    IPublicKey,
    KholawEd25519PublicKey,
    SLIP10Ed25519PublicKey,
    SLIP10Ed25519Blake2bPublicKey,
    SLIP10Ed25519MoneroPublicKey,
    SLIP10Nist256p1PublicKey,
    SLIP10Secp256k1PublicKey
)


class IAddress(ABC):

    @classmethod
    @abstractmethod
    def encode(cls, public_key: Union[bytes, IPublicKey], *args, **kwargs: Any) -> str:
        pass

    @classmethod
    @abstractmethod
    def decode(cls, address: str, **kwargs: Any) -> bytes:
        pass


def validate_and_get_public_key(
    public_key: Union[bytes, str, IPublicKey], public_key_cls: Type[IPublicKey]
) -> Union[
    IPublicKey,
    KholawEd25519PublicKey,
    SLIP10Ed25519PublicKey,
    SLIP10Ed25519Blake2bPublicKey,
    SLIP10Ed25519MoneroPublicKey,
    SLIP10Nist256p1PublicKey,
    SLIP10Secp256k1PublicKey
]:
    if isinstance(public_key, bytes):
        public_key: IPublicKey = public_key_cls.from_bytes(public_key)
    elif isinstance(public_key, str):
        public_key: IPublicKey = public_key_cls.from_bytes(unhexlify(public_key))
    elif not isinstance(public_key, public_key_cls):
        ecc: EllipticCurveCryptography = ECC_TYPE_TO_INSTANCE[public_key_cls.curve_type()]
        raise TypeError(f"A {ecc.curve_name()} public key is required"
                        f"(expected: {public_key_cls}, got: {type(public_key)}")
    return public_key
