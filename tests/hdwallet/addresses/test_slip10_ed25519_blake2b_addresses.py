#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import os
import pytest

from hdwallet.addresses.nano import NanoAddress

# Test Values
base_path: str = os.path.dirname(__file__)
file_path: str = os.path.abspath(os.path.join(base_path, "../../data/addresses.json"))
values = open(file_path, "r", encoding="utf-8")
_: dict = json.loads(values.read())
values.close()


def test_nano_address():

    assert NanoAddress.name() == _["SLIP10-Ed25519-Blake2b"]["addresses"]["Nano"]["name"]
    assert NanoAddress.encode(
        public_key=_["SLIP10-Ed25519-Blake2b"]["public-key"]
    ) == _["SLIP10-Ed25519-Blake2b"]["addresses"]["Nano"]["encode"]

    assert NanoAddress.decode(
        address=_["SLIP10-Ed25519-Blake2b"]["addresses"]["Nano"]["encode"]
    ) == _["SLIP10-Ed25519-Blake2b"]["addresses"]["Nano"]["decode"]

