#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Optional, Union, Tuple
)

from ..libs.ed25519 import scalar_reduce, int_decode
from ..ecc import (
    SLIP10Ed25519MoneroECC, IPoint, IPublicKey, IPrivateKey, SLIP10Ed25519MoneroPublicKey, SLIP10Ed25519MoneroPrivateKey
)
from ..crypto import kekkak256
from ..utils import (
    get_bytes, bytes_to_string, integer_to_bytes, bytes_to_integer
)
from ..addresses.monero import MoneroAddress
from .ihd import IHD


class MoneroHD(IHD):

    _network: str
    _seed: Optional[bytes] = None
    _private_key: Optional[bytes] = None

    _spend_private_key: Optional[IPrivateKey]
    _view_private_key: Union[IPrivateKey]
    _spend_public_key: Union[IPublicKey]
    _view_public_key: Union[IPublicKey]

    def __init__(self, network: str = "mainnet", **kwargs) -> None:
        super().__init__(**kwargs)

        if network not in ["mainnet", "stagenet", "testnet"]:
            raise ValueError(f"Invalid network type, (expected: 'mainnet', 'stagenet', or 'testnet' networks, got: '{network}')")

        self._network = network

    @classmethod
    def name(cls) -> str:
        return "Monero"

    def from_seed(self, seed: Union[bytes, str], **kwargs) -> "MoneroHD":

        self._seed = seed
        spend_private_key: bytes = (
            get_bytes(seed) if len(get_bytes(seed)) == SLIP10Ed25519MoneroPrivateKey.length() else kekkak256(get_bytes(seed))
        )
        return self.from_spend_private_key(
            spend_private_key=scalar_reduce(spend_private_key)
        )

    def from_private_key(self, private_key: Union[bytes, str, IPrivateKey]) -> "MoneroHD":

        self._private_key = (
            private_key.raw() if isinstance(private_key, SLIP10Ed25519MoneroPrivateKey) else get_bytes(private_key)
        )
        return self.from_spend_private_key(
            spend_private_key=scalar_reduce(kekkak256(self._private_key))
        )

    def from_spend_private_key(self, spend_private_key: Union[bytes, str, IPrivateKey]) -> "MoneroHD":

        if isinstance(spend_private_key, (bytes, str)):
            spend_private_key: IPrivateKey = SLIP10Ed25519MoneroPrivateKey.from_bytes(get_bytes(spend_private_key))

        self._spend_private_key = spend_private_key
        self._view_private_key = SLIP10Ed25519MoneroPrivateKey.from_bytes(
            scalar_reduce(kekkak256(spend_private_key.raw()))
        )
        self._spend_public_key = self._spend_private_key.public_key()
        self._view_public_key = self._view_private_key.public_key()
        return self

    def from_watch_only(
        self, view_private_key: Union[bytes, str, IPrivateKey], spend_public_key: Union[bytes, str, IPublicKey]
    ) -> "MoneroHD":

        if isinstance(view_private_key, (bytes, str)):
            view_private_key: IPrivateKey = SLIP10Ed25519MoneroPrivateKey.from_bytes(get_bytes(view_private_key))
        if isinstance(spend_public_key, (bytes, str)):
            spend_public_key: IPublicKey = SLIP10Ed25519MoneroPublicKey.from_bytes(get_bytes(spend_public_key))

        self._spend_private_key = None
        self._view_private_key = view_private_key
        self._spend_public_key = spend_public_key
        self._view_public_key = self._view_private_key.public_key()
        return self

    def drive(self, minor_index: int, major_index: int) -> Tuple[IPublicKey, IPublicKey]:

        maximum_index: int = 2 ** 32 - 1
        if minor_index < 0 or minor_index > maximum_index:
            raise ValueError(f"Invalid minor index (expected: 0-{maximum_index}, got: {minor_index})")
        if major_index < 0 or major_index > maximum_index:
            raise ValueError(f"Invalid major index (expected: 0-{maximum_index}, got: {major_index})")

        if minor_index == 0 and major_index == 0:
            return self._spend_public_key, self._view_public_key

        m: int = int_decode(scalar_reduce(
            kekkak256(
                b"SubAddr\x00" +
                self._view_private_key.raw() +
                integer_to_bytes(
                    major_index, bytes_num=4, endianness="little"
                ) + integer_to_bytes(
                    minor_index, bytes_num=4, endianness="little"
                )
            )
        ))

        sub_address_spend_public_key: IPoint = (
            self._spend_public_key.point() + (SLIP10Ed25519MoneroECC.GENERATOR * m)
        )
        sub_address_view_public_key: IPoint = (
            sub_address_spend_public_key * bytes_to_integer(
                self._view_private_key.raw(), endianness="little"
            )
        )

        return (
            SLIP10Ed25519MoneroPublicKey.from_point(sub_address_spend_public_key),
            SLIP10Ed25519MoneroPublicKey.from_point(sub_address_view_public_key)
        )

    def seed(self) -> Optional[str]:
        return bytes_to_string(self._seed) if self._seed else None

    def private_key(self) -> Optional[str]:
        return bytes_to_string(self._private_key) if self._private_key else None

    def spend_private_key(self) -> Optional[str]:
        return bytes_to_string(self._spend_private_key.raw()) if self._spend_private_key else None

    def view_private_key(self) -> str:
        return bytes_to_string(
            self._view_private_key.raw()
        )

    def spend_public_key(self) -> str:
        return bytes_to_string(self._spend_public_key.raw_compressed())

    def view_public_key(self) -> str:
        return bytes_to_string(self._view_public_key.raw_compressed())

    def primary_address(self) -> str:
        return MoneroAddress.encode(
            spend_public_key=self._spend_public_key,
            view_public_key=self._view_public_key,
            network_type=self._network,
            version_type="standard",
            payment_id=None
        )

    def integrated_address(self, payment_id: Union[bytes, str]) -> str:
        return MoneroAddress.encode(
            spend_public_key=self._spend_public_key,
            view_public_key=self._view_public_key,
            network_type=self._network,
            version_type="integrated",
            payment_id=get_bytes(payment_id)
        )

    def sub_address(self, minor_index: int, major_index: int = 0) -> str:

        if minor_index == 0 and major_index == 0:
            return self.primary_address()

        spend_public_key, view_public_key = self.drive(
            minor_index=minor_index, major_index=major_index
        )

        return MoneroAddress.encode(
            spend_public_key=spend_public_key,
            view_public_key=view_public_key,
            network_type=self._network,
            version_type="sub-address",
            payment_id=None
        )

    def address(self, version_type: str, **kwargs) -> str:

        if version_type == "standard":
            return self.primary_address()
        elif version_type == "integrated":
            return self.integrated_address(
                payment_id=kwargs.get("payment_id")
            )
        elif version_type == "sub-address":
            return self.sub_address(
                minor_index=kwargs.get("minor_index"), major_index=kwargs.get("major_index", 0)
            )
        raise ValueError(
            f"Invalid version type, (expected: 'standard', 'integrated', and 'sub-address' types, got: '{version_type}')"
        )
