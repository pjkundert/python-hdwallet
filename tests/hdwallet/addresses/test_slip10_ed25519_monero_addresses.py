#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import os
import pytest

from hdwallet.addresses.monero import MoneroAddress

# Test Values
base_path: str = os.path.dirname(__file__)
file_path: str = os.path.abspath(os.path.join(base_path, "../../data/addresses.json"))
values = open(file_path, "r", encoding="utf-8")
_: dict = json.loads(values.read())
values.close()


def test_monero_address():

    assert MoneroAddress.name() == _["SLIP10-Ed25519-Monero"]["name"]
    assert MoneroAddress.encode(
        spend_public_key=_["SLIP10-Ed25519-Monero"]["spend-public-key"],
        view_public_key=_["SLIP10-Ed25519-Monero"]["view-public-key"],
        payment_id=_["SLIP10-Ed25519-Monero"]["args"]["payment_id"]
    ) == _["SLIP10-Ed25519-Monero"]["encode"]

    spend_public_key, view_public_key = MoneroAddress.decode(
        address=_["SLIP10-Ed25519-Monero"]["encode"],
        payment_id=_["SLIP10-Ed25519-Monero"]["args"]["payment_id"]
    )
    assert spend_public_key == _["SLIP10-Ed25519-Monero"]["spend-public-key"]
    assert view_public_key == _["SLIP10-Ed25519-Monero"]["view-public-key"]
