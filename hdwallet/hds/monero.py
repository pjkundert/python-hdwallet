#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Optional, Union, Tuple, Type
)

from ..libs.ed25519 import scalar_reduce, int_decode
from ..ecc import (
    SLIP10Ed25519MoneroECC, IPoint, IPublicKey, IPrivateKey, SLIP10Ed25519MoneroPublicKey, SLIP10Ed25519MoneroPrivateKey
)
from ..seeds import ISeed
from ..crypto import kekkak256
from ..cryptocurrencies.icryptocurrency import INetwork
from ..cryptocurrencies import Monero
from ..derivations import (
    IDerivation, MoneroDerivation
)
from ..exceptions import (
    NetworkError, DerivationError, AddressError
)
from ..utils import (
    get_bytes, bytes_to_string, integer_to_bytes, bytes_to_integer
)
from ..addresses import MoneroAddress
from .ihd import IHD


class MoneroHD(IHD):

    _network: INetwork
    _seed: Optional[bytes] = None
    _private_key: Optional[bytes] = None

    _spend_private_key: Optional[IPrivateKey]
    _view_private_key: Union[IPrivateKey]
    _spend_public_key: Union[IPublicKey]
    _view_public_key: Union[IPublicKey]

    _derivation: MoneroDerivation

    def __init__(self, network: Union[str, Type[INetwork]] = "mainnet", **kwargs) -> None:
        super().__init__(**kwargs)

        try:
            if not isinstance(network, str) and issubclass(network, INetwork):
                network = network.__name__.lower()
            if not Monero.NETWORKS.is_network(network=network):
                raise NetworkError(
                    f"Wrong {Monero.NAME} network",
                    expected=Monero.NETWORKS.get_networks(),
                    got=network
                )
            self._network = Monero.NETWORKS.get_network(network=network)
        except TypeError:
            raise NetworkError(
                "Invalid network type", expected=[str, INetwork], got=type(network)
            )

        self._derivation = MoneroDerivation(
            minor=kwargs.get("minor", 1), major=kwargs.get("major", 0)
        )

    @classmethod
    def name(cls) -> str:
        return "Monero"

    def __update__(self) -> "MoneroHD":
        self.from_derivation(derivation=self._derivation)
        return self

    def from_seed(self, seed: Union[bytes, str, ISeed], **kwargs) -> "MoneroHD":

        self._seed = get_bytes(
            seed.seed() if isinstance(seed, ISeed) else seed
        )
        spend_private_key: bytes = (
            self._seed if len(self._seed) == SLIP10Ed25519MoneroPrivateKey.length() else kekkak256(self._seed)
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

    def from_derivation(self, derivation: IDerivation) -> "MoneroHD":

        if not isinstance(derivation, MoneroDerivation):
            raise DerivationError(
                f"Invalid {self.name()} derivation instance", expected=MoneroDerivation, got=type(derivation)
            )

        self._derivation = derivation
        return self

    def update_derivation(self, derivation: IDerivation) -> "MoneroHD":
        return self.from_derivation(derivation=derivation)

    def clean_derivation(self) -> "MoneroHD":
        self._derivation.clean()
        self.__update__()
        return self

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
            raise DerivationError(
                f"Invalid minor index range", expected=f"0-{maximum_index}", got=minor_index
            )
        if major_index < 0 or major_index > maximum_index:
            raise DerivationError(
                f"Invalid major index range", expected=f"0-{maximum_index}", got=major_index
            )

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
            network=self._network.__name__.lower(),
            address_type=Monero.ADDRESS_TYPES.STANDARD,
            payment_id=None
        )

    def integrated_address(self, payment_id: Union[bytes, str]) -> str:
        return MoneroAddress.encode(
            spend_public_key=self._spend_public_key,
            view_public_key=self._view_public_key,
            network=self._network.__name__.lower(),
            address_type=Monero.ADDRESS_TYPES.INTEGRATED,
            payment_id=get_bytes(payment_id)
        )

    def sub_address(self, minor: Optional[int] = None, major: Optional[int] = None) -> str:

        if minor is None and major is None:
            minor, major = self._derivation.minor(), self._derivation.major()
        elif (minor and major is None) or (minor is None and major):
            raise DerivationError("Both minor and major indexes are required")

        if minor == 0 and major == 0:
            return self.primary_address()

        spend_public_key, view_public_key = self.drive(
            minor_index=minor, major_index=major
        )

        return MoneroAddress.encode(
            spend_public_key=spend_public_key,
            view_public_key=view_public_key,
            network=self._network.__name__.lower(),
            address_type="sub-address",
            payment_id=None
        )

    def address(self, address_type: str, **kwargs) -> str:

        if address_type == Monero.ADDRESS_TYPES.STANDARD:
            return self.primary_address()
        elif address_type == Monero.ADDRESS_TYPES.INTEGRATED:
            return self.integrated_address(
                payment_id=kwargs.get("payment_id")
            )
        elif address_type == Monero.ADDRESS_TYPES.SUB_ADDRESS:
            return self.sub_address(
                minor=kwargs.get("minor", self._derivation.minor()),
                major=kwargs.get("major", self._derivation.major())
            )
        raise AddressError(
            f"Invalid {self.name()} address type",
            expected=Monero.ADDRESS_TYPES.get_address_types(),
            got=address_type
        )
