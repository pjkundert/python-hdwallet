#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Union, Optional
)

from ...addresses.p2pkh import P2PKHAddress
from ...addresses.p2wpkh import P2WPKHAddress
from ...derivations.custom import CustomDerivation
from ...wif import private_key_to_wif
from ...derivations import (
    IDerivation, ElectrumDerivation
)
from ...cryptocurrencies import Bitcoin
from ...const import (
    PUBLIC_KEY_TYPES, ELECTRUM_V2_MODES, WIF_TYPES
)
from ..bip32 import BIP32HD
from ..ihd import IHD


class ElectrumV2HD(IHD):

    _mode: str
    _wif_type: str
    _public_key_type: str

    def __init__(
        self, mode: str = ELECTRUM_V2_MODES.STANDARD, public_key_type: str = PUBLIC_KEY_TYPES.UNCOMPRESSED, **kwargs
    ) -> None:
        super().__init__(**kwargs)

        if mode not in ELECTRUM_V2_MODES.get_modes():
            raise ValueError(
                f"Invalid Electrum-V2 mode, (expected: '{ELECTRUM_V2_MODES.get_modes()}', got: '{mode}')"
            )
        self._mode = mode

        if public_key_type == PUBLIC_KEY_TYPES.UNCOMPRESSED:
            self._wif_type = WIF_TYPES.WIF
        elif public_key_type == PUBLIC_KEY_TYPES.COMPRESSED:
            self._wif_type = WIF_TYPES.WIF_COMPRESSED
        else:
            raise ValueError(
                f"Invalid public key type, (expected: '{PUBLIC_KEY_TYPES.get_types()}', got: '{public_key_type}')"
            )
        self._public_key_type = public_key_type
        self._bip32_hd: BIP32HD = BIP32HD(
            ecc_name="SLIP10-Secp256k1", public_key_type=self._public_key_type
        )

    @classmethod
    def name(cls) -> str:
        return "Electrum-V2"

    def from_seed(self, seed: Union[bytes, str], **kwargs) -> "ElectrumV2HD":
        self._bip32_hd.from_seed(seed=seed)
        return self

    def master_private_key(self) -> Optional[str]:
        return self._bip32_hd.root_private_key()

    def master_public_key(self) -> str:
        return self._bip32_hd.root_public_key(public_key_type=self._public_key_type)
    
    def update_derivation(self, derivation: IDerivation) -> "ElectrumV2HD":

        if not isinstance(derivation, ElectrumDerivation):
            raise TypeError(
                f"Invalid Electrum-V2 derivation type, (expected: '{ElectrumDerivation.name()}', got: '{derivation.name()}')"
            )
        return self.drive(
            change_index=derivation.change(only_index=True),
            address_index=derivation.address(only_index=True)
        )

    def drive(self, change_index: int, address_index: int) -> "ElectrumV2HD":
        custom_derivation: CustomDerivation = CustomDerivation()
        if self._mode == ELECTRUM_V2_MODES.SEGWIT:
            custom_derivation.from_index(index=0, hardened=True)
        custom_derivation.from_index(index=change_index)  # Change index
        custom_derivation.from_index(index=address_index)  # Address index
        self._bip32_hd.update_derivation(derivation=custom_derivation)
        return self

    def mode(self) -> str:
        return self._mode

    def private_key(self) -> Optional[str]:
        return self._bip32_hd.private_key()

    def wif(self, wif_type: Optional[str] = None) -> Optional[str]:
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
        return self._bip32_hd.public_key(
            public_key_type=public_key_type
        )

    def public_key_type(self) -> str:
        return self._public_key_type

    def uncompressed(self) -> str:
        return self._bip32_hd.uncompressed()

    def compressed(self) -> str:
        return self._bip32_hd.compressed()

    def address(
        self,
        network_version: int = Bitcoin.NETWORKS.MAINNET.PUBLIC_KEY_ADDRESS_PREFIX,
        hrp: str = Bitcoin.NETWORKS.MAINNET.HRP,
        witness_version: str = Bitcoin.NETWORKS.MAINNET.WITNESS_VERSIONS.P2WPKH,
    ) -> str:

        if self._mode == ELECTRUM_V2_MODES.STANDARD:
            return P2PKHAddress.encode(
                public_key=self.public_key(), network_version=network_version, public_key_type=self._public_key_type
            )
        elif self._mode == ELECTRUM_V2_MODES.SEGWIT:
            return P2WPKHAddress.encode(
                public_key=self.public_key(), hrp=hrp, witness_version=witness_version
            )
