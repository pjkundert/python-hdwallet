#!/usr/bin/env python3

# Copyright © 2023, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from .ethereum import EthereumAddress


class XinFinAddress(EthereumAddress):

    address_prefix: str = "xdc"
