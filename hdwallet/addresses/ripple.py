#!/usr/bin/env python3

from .p2pkh import P2PKHAddress


class RippleAddress(P2PKHAddress):

    alphabet: bytes = b"rpshnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCg65jkm8oFqi1tuvAxyz"
