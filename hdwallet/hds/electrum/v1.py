#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Union, Optional
)

from ...ecc import (
    IPublicKey, IPrivateKey
)
from ...ecc.slip10.secp256k1 import (
    SLIP10Secp256k1ECC, SLIP10Secp256k1PrivateKey, SLIP10Secp256k1PublicKey
)
from ...addresses.p2pkh import P2PKHAddress
from ...wif import (
    private_key_to_wif, wif_to_private_key
)
from ...const import PUBLIC_KEY_TYPES
from ...derivations import (
    IDerivation, ElectrumDerivation
)
from ...crypto import double_sha256
from ...cryptocurrencies import Bitcoin
from ...exceptions import DerivationError
from ...utils import (
    get_bytes, encode, bytes_to_string, bytes_to_integer, integer_to_bytes
)
from ...wif import WIF_TYPES
from ..ihd import IHD


class ElectrumV1HD(IHD):

    _master_private_key: Optional[IPrivateKey]
    _master_public_key: IPublicKey
    _private_key: Optional[IPrivateKey]
    _wif_type: str
    _public_key: IPublicKey
    _public_key_type: str

    def __init__(self, public_key_type: str = PUBLIC_KEY_TYPES.UNCOMPRESSED, **kwargs) -> None:
        super().__init__(**kwargs)

        if public_key_type == PUBLIC_KEY_TYPES.UNCOMPRESSED:
            self._wif_type = WIF_TYPES.WIF
        elif public_key_type == PUBLIC_KEY_TYPES.COMPRESSED:
            self._wif_type = WIF_TYPES.WIF_COMPRESSED
        else:
            raise ValueError(
                f"Invalid public key type, (expected: '{PUBLIC_KEY_TYPES.get_types()}', got: '{public_key_type}')"
            )
        self._public_key_type = public_key_type
        self._master_private_key = None
        self._private_key = None

    @classmethod
    def name(cls) -> str:
        return "Electrum-V1"

    def from_seed(self, seed: Union[bytes, str], **kwargs) -> "ElectrumV1HD":
        return self.from_private_key(private_key=seed)

    def from_private_key(self, private_key: Union[bytes, str, IPrivateKey]) -> "ElectrumV1HD":

        if not isinstance(private_key, SLIP10Secp256k1PrivateKey):
            private_key: IPrivateKey = SLIP10Secp256k1PrivateKey.from_bytes(
                get_bytes(private_key)
            )

        self._master_private_key, self._master_public_key = (
            private_key, private_key.public_key()
        )
        return self

    def from_wif(self, wif: str) -> "ElectrumV1HD":
        return self.from_private_key(
            private_key=wif_to_private_key(wif=wif)
        )

    def from_public_key(self, public_key: Union[bytes, str, IPublicKey]) -> "ElectrumV1HD":

        if not isinstance(public_key, SLIP10Secp256k1PublicKey):
            public_key: IPublicKey = SLIP10Secp256k1PublicKey.from_bytes(
                get_bytes(public_key)
            )

        self._master_public_key = public_key
        return self

    def master_private_key(self) -> Optional[str]:

        if not self._master_private_key:
            return None

        return bytes_to_string(self._master_private_key.raw())

    def master_public_key(self, public_key_type: Optional[str] = None) -> str:
        _public_key_type: str = (
            public_key_type if public_key_type in PUBLIC_KEY_TYPES.get_types() else self._public_key_type
        )
        if _public_key_type == PUBLIC_KEY_TYPES.UNCOMPRESSED:
            return bytes_to_string(self._master_public_key.raw_uncompressed())
        elif _public_key_type == PUBLIC_KEY_TYPES.COMPRESSED:
            return bytes_to_string(self._master_public_key.raw_compressed())
        raise ValueError("Invalid public key type")

    def update_derivation(self, derivation: IDerivation) -> "ElectrumV1HD":

        if not isinstance(derivation, ElectrumDerivation):
            raise DerivationError(
                f"Invalid Electrum V1 derivation instance", expected=ElectrumDerivation.name(), got=derivation.name()
            )
        return self.drive(
            change_index=(
                derivation.change()[1]
                if len(derivation.change()) == 3 else
                derivation.change()[0]
            ),
            address_index=(
                derivation.address()[1]
                if len(derivation.address()) == 3 else
                derivation.address()[0]
            )
        )

    def drive(self, change_index: int, address_index: int) -> "ElectrumV1HD":

        sequence: bytes = double_sha256(
            encode(f"{address_index}:{change_index}:") + self._master_public_key.raw_uncompressed()[1:]
        )

        if self._master_private_key:
            private_key: int = (
                bytes_to_integer(self._master_private_key.raw()) + bytes_to_integer(sequence)
            ) % SLIP10Secp256k1ECC.ORDER
            self._private_key = SLIP10Secp256k1PrivateKey.from_bytes(
                integer_to_bytes(private_key, bytes_num=SLIP10Secp256k1PrivateKey.length())
            )
            self._public_key = self._private_key.public_key()
        else:
            self._public_key = SLIP10Secp256k1PublicKey.from_point(
                self._master_public_key.point() + bytes_to_integer(sequence) * SLIP10Secp256k1ECC.GENERATOR
            )
        return self

    def private_key(self) -> Optional[str]:
        if not self._private_key:
            return None
        return bytes_to_string(self._private_key.raw())

    def wif(self, wif_type: Optional[str] = None) -> Optional[str]:
        if not self._private_key:
            return None

        if wif_type:
            if wif_type not in WIF_TYPES.get_types():
                raise Exception(
                    f"Invalid WIF type, (expected: '{WIF_TYPES.get_types()}', got: '{wif_type}')"
                )
            _wif_type: str = wif_type
        else:
            _wif_type: str = self._wif_type

        return private_key_to_wif(
            private_key=self.private_key(), wif_type=_wif_type
        )

    def wif_type(self) -> str:
        return self._wif_type

    def public_key(self, public_key_type: Optional[str] = None) -> str:
        if public_key_type:
            if public_key_type not in PUBLIC_KEY_TYPES.get_types():
                raise Exception(
                    f"Invalid public key type, (expected: '{PUBLIC_KEY_TYPES.get_types()}', got: '{public_key_type}')"
                )
            _public_key_type: str = public_key_type
        else:
            _public_key_type: str = self._public_key_type

        if _public_key_type == PUBLIC_KEY_TYPES.UNCOMPRESSED:
            return self.uncompressed()
        elif _public_key_type == PUBLIC_KEY_TYPES.COMPRESSED:
            return self.compressed()

    def public_key_type(self) -> str:
        return self._public_key_type

    def uncompressed(self) -> str:
        return bytes_to_string(self._public_key.raw_uncompressed())

    def compressed(self) -> str:
        return bytes_to_string(self._public_key.raw_compressed())

    def address(self, network_version: int = Bitcoin.NETWORKS.MAINNET.PUBLIC_KEY_ADDRESS_PREFIX) -> str:

        return P2PKHAddress.encode(
            public_key=self._public_key, network_version=network_version, public_key_type=self._public_key_type
        )
