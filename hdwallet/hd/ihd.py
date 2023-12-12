#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Union


class IHD:

    def name(self) -> str:
        pass

    def from_seed(self, seed: Union[bytes, str], **kwargs) -> "IHD":
        pass

    def address(self, **kwargs) -> str:
        pass
