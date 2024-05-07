#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Type, Union, Optional
)

from ..cryptocurrencies import Bitcoin
from ..ecc import IEllipticCurveCryptography
from ..const import PUBLIC_KEY_TYPES
from ..addresses import (
    P2WPKHAddress, P2WPKHInP2SHAddress, P2WSHAddress, P2WSHInP2SHAddress
)
from ..exceptions import (
    Error, AddressError
)
from .bip32 import BIP32HD


class BIP141HD(BIP32HD):

    _address: str
    _xprivate_key_version: Union[bytes, int]
    _xpublic_key_version: Union[bytes, int]
    _semantic: str

    def __init__(
        self,
        ecc: Type[IEllipticCurveCryptography],
        semantic: str,
        public_key_type: str = PUBLIC_KEY_TYPES.COMPRESSED,
        **kwargs
    ) -> None:
        super(BIP141HD, self).__init__(ecc=ecc, public_key_type=public_key_type, **kwargs)

        self.from_semantic(semantic=semantic, **kwargs)

    @classmethod
    def name(cls) -> str:
        return "BIP141"

    def from_semantic(self, semantic: str, **kwargs) -> "BIP141HD":

        if semantic not in [
            "P2WPKH", "P2WPKH_IN_P2SH", "P2WSH", "P2WSH_IN_P2SH"
        ]:
            raise Error(f"Invalid {self.name()} semantic type", expected=[
                "P2WPKH", "P2WPKH_IN_P2SH", "P2WSH", "P2WSH_IN_P2SH"
            ], got=semantic)
        self._semantic = semantic

        if semantic == "P2WPKH":
            self._address = P2WPKHAddress.name()
            self._xprivate_key_version = kwargs.get(
                "p2wpkh_xprivate_key_version", Bitcoin.NETWORKS.MAINNET.XPRIVATE_KEY_VERSIONS.P2WPKH
            )
            self._xpublic_key_version = kwargs.get(
                "p2wpkh_xpublic_key_version", Bitcoin.NETWORKS.MAINNET.XPUBLIC_KEY_VERSIONS.P2WPKH
            )
        elif semantic == "P2WPKH_IN_P2SH":
            self._address = P2WPKHInP2SHAddress.name()
            self._xprivate_key_version = kwargs.get(
                "p2wpkh_in_p2sh_xprivate_key_version", Bitcoin.NETWORKS.MAINNET.XPRIVATE_KEY_VERSIONS.P2WPKH_IN_P2SH
            )
            self._xpublic_key_version = kwargs.get(
                "p2wpkh_in_p2sh_xpublic_key_version", Bitcoin.NETWORKS.MAINNET.XPUBLIC_KEY_VERSIONS.P2WPKH_IN_P2SH
            )
        elif semantic == "P2WSH":
            self._address = P2WSHAddress.name()
            self._xprivate_key_version = kwargs.get(
                "p2wsh_xprivate_key_version", Bitcoin.NETWORKS.MAINNET.XPRIVATE_KEY_VERSIONS.P2WSH
            )
            self._xpublic_key_version = kwargs.get(
                "p2wsh_xpublic_key_version", Bitcoin.NETWORKS.MAINNET.XPUBLIC_KEY_VERSIONS.P2WSH
            )
        elif semantic == "P2WSH_IN_P2SH":
            self._address = P2WSHInP2SHAddress.name()
            self._xprivate_key_version = kwargs.get(
                "p2wsh_in_p2sh_xprivate_key_version", Bitcoin.NETWORKS.MAINNET.XPRIVATE_KEY_VERSIONS.P2WSH_IN_P2SH
            )
            self._xpublic_key_version = kwargs.get(
                "p2wsh_in_p2sh_xpublic_key_version", Bitcoin.NETWORKS.MAINNET.XPUBLIC_KEY_VERSIONS.P2WSH_IN_P2SH
            )
        return self

    def semantic(self) -> str:
        return self._semantic

    def root_xprivate_key(
        self, version: Optional[Union[bytes, int]] = None, encoded: bool = True
    ) -> Optional[str]:
        return super(BIP141HD, self).root_xprivate_key(
            version=(self._xprivate_key_version if version is None else version), encoded=encoded
        )

    def root_xpublic_key(
        self, version: Optional[Union[bytes, int]] = None, encoded: bool = True
    ) -> Optional[str]:
        return super(BIP141HD, self).root_xpublic_key(
            version=(self._xpublic_key_version if version is None else version), encoded=encoded
        )

    def xprivate_key(
        self, version: Optional[Union[bytes, int]] = None, encoded: bool = True
    ) -> Optional[str]:
        return super(BIP141HD, self).xprivate_key(
            version=(self._xprivate_key_version if version is None else version), encoded=encoded
        )

    def xpublic_key(
        self, version: Optional[Union[bytes, int]] = None, encoded: bool = True
    ) -> Optional[str]:
        return super(BIP141HD, self).xpublic_key(
            version=(self._xpublic_key_version if version is None else version) , encoded=encoded
        )

    def address(
        self,
        address: Optional[str] = None,
        script_address_prefix: int = Bitcoin.NETWORKS.MAINNET.SCRIPT_ADDRESS_PREFIX,
        hrp: str = Bitcoin.NETWORKS.MAINNET.HRP,
        witness_version: int = Bitcoin.NETWORKS.MAINNET.WITNESS_VERSIONS.P2WPKH,
        **kwargs
    ) -> str:
        if address is None:
            address = self._address
        if address == P2WPKHAddress.name():
            return P2WPKHAddress.encode(
                public_key=self._public_key,
                hrp=hrp,
                witness_version=witness_version,
                public_key_type=self._public_key_type
            )
        elif address == P2WPKHInP2SHAddress.name():
            return P2WPKHInP2SHAddress.encode(
                public_key=self._public_key,
                script_address_prefix=script_address_prefix,
                public_key_type=self._public_key_type
            )
        elif address == P2WSHAddress.name():
            return P2WSHAddress.encode(
                public_key=self._public_key,
                hrp=hrp,
                witness_version=witness_version,
                public_key_type=self._public_key_type
            )
        elif address == P2WSHInP2SHAddress.name():
            return P2WSHInP2SHAddress.encode(
                public_key=self._public_key,
                script_address_prefix=script_address_prefix,
                public_key_type=self._public_key_type
            )
        raise AddressError(
            f"Invalid {self.name()} address",
            expected=[
                P2WPKHAddress.name(),
                P2WPKHInP2SHAddress.name(),
                P2WSHAddress.name(),
                P2WSHInP2SHAddress.name()
            ],
            got=self._address
        )
