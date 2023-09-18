#!/usr/bin/env python3

from .ethereum import EthereumAddress


class XinFinAddress(EthereumAddress):

    address_prefix: str = "xdc"
