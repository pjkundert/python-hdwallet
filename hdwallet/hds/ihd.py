#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Union, List, Optional
)

from ..derivations import IDerivation


class IHD:

    def __init__(self, **kwargs) -> None:
        pass

    @classmethod
    def name(cls) -> str:
        pass

    def from_seed(self, seed: Union[bytes, str], **kwargs) -> "IHD":
        pass

    def from_xprivate_key(
        self, xprivate_key: str, encoded: bool = True, strict: bool = False
    ) -> "IHD":
        pass

    def from_xpublic_key(
        self, xpublic_key: str, encoded: bool = True, strict: bool = False
    ) -> "IHD":
        pass

    def from_wif(self, wif: str) -> "IHD":
        pass

    def from_private_key(self, private_key: str) -> "IHD":
        pass

    def from_spend_private_key(self, spend_private_key: str) -> "IHD":
        pass

    def from_public_key(self, public_key: str) -> "IHD":
        pass

    def from_watch_only(self, view_private_key, spend_public_key) -> "IHD":
        pass

    def from_derivation(self, derivation: IDerivation) -> "IHD":
        pass

    def update_derivation(self, derivation: IDerivation) -> "IHD":
        pass

    def clean_derivation(self) -> "IHD":
        pass

    def seed(self) -> Optional[str]:
        pass

    def semantic(self) -> Optional[str]:
        return None

    def root_xprivate_key(self, *args, **kwargs) -> Optional[str]:
        pass

    def root_xpublic_key(self, *args, **kwargs) -> Optional[str]:
        pass

    def master_xprivate_key(self, *args, **kwargs) -> Optional[str]:
        return self.root_xprivate_key(args, kwargs)

    def master_xpublic_key(self, *args, **kwargs) -> Optional[str]:
        return self.root_xpublic_key(args, kwargs)

    def root_private_key(self, *args, **kwargs) -> Optional[str]:
        pass

    def root_wif(self, *args, **kwargs) -> Optional[str]:
        pass

    def root_chain_code(self) -> Optional[str]:
        pass

    def root_public_key(self, *args, **kwargs) -> Optional[str]:
        pass

    def master_private_key(self, *args, **kwargs) -> Optional[str]:
        pass

    def master_wif(self, *args, **kwargs) -> Optional[str]:
        pass

    def master_chain_code(self) -> Optional[str]:
        return self.root_chain_code()

    def master_public_key(self, *args, **kwargs) -> str:
        pass

    def xprivate_key(self, *args, **kwargs) -> Optional[str]:
        pass

    def xpublic_key(self, *args, **kwargs) -> Optional[str]:
        pass

    def private_key(self, *args, **kwargs) -> Optional[str]:
        pass

    def spend_private_key(self) -> str:
        pass

    def view_private_key(self) -> str:
        pass

    def wif(self, *args, **kwargs) -> Optional[str]:
        pass

    def wif_type(self) -> str:
        pass

    def chain_code(self) -> str:
        pass

    def public_key(self, *args, **kwargs) -> str:
        pass

    def compressed(self) -> str:
        pass

    def uncompressed(self) -> str:
        pass

    def spend_public_key(self) -> str:
        pass

    def view_public_key(self) -> str:
        pass

    def public_key_type(self) -> str:
        pass

    def mode(self) -> str:
        pass

    def hash(self) -> str:
        pass

    def fingerprint(self) -> str:
        pass

    def parent_fingerprint(self) -> str:
        pass

    def depth(self) -> int:
        pass

    def path(self) -> str:
        pass

    def path_key(self) -> str:
        pass

    def index(self) -> int:
        pass

    def indexes(self) -> List[int]:
        pass

    def strict(self) -> Optional[bool]:
        pass

    def integrated_address(self, **kwargs) -> str:
        pass

    def primary_address(self, **kwargs) -> str:
        pass

    def sub_address(self, **kwargs) -> str:
        pass

    def address(self, **kwargs) -> str:
        pass
