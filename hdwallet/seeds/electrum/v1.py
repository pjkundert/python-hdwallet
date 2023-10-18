#!/usr/bin/env python3

# Copyright © 2020-2023, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from ...utils import bytes_to_string, encode
from ...crypto import sha256
from ...mnemonics.electrum.v1 import ElectrumV1Mnemonic
from .. import ISeed


class ElectrumV1Seed(ISeed):

    # Number of hash iteration
    hash_iteration_number: int = 10 ** 5

    @classmethod
    def generate(cls, mnemonic: str, **kwargs) -> str:

        if not ElectrumV1Mnemonic.is_valid(mnemonic=mnemonic):
            ValueError("Invalid Electrum V1 mnemonic words")

        entropy: str = ElectrumV1Mnemonic.decode(mnemonic)
        entropy_hash: bytes = encode(entropy)
        for _ in range(cls.hash_iteration_number):
            entropy_hash = sha256(entropy_hash + encode(entropy))

        return bytes_to_string(entropy_hash)
