#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import os
import pytest

from hdwallet.derivations.monero import MoneroDerivation
from hdwallet.exceptions import DerivationError

# Test Values
base_path: str = os.path.dirname(__file__)
file_path: str = os.path.abspath(os.path.join(base_path, "../../data/derivations.json"))
values = open(file_path, "r", encoding="utf-8")
_: dict = json.loads(values.read())
values.close()

def test_monero_derivation():

    derivation = MoneroDerivation()
    assert derivation.name() == _["Monero"]["default"]["name"]
    assert derivation.minor() == _["Monero"]["default"]["minor"]
    assert derivation.major() == _["Monero"]["default"]["major"]

    derivation = MoneroDerivation(
        minor=_["Monero"]["from"]["minor"],
        major=_["Monero"]["from"]["major"]

    )
    assert derivation.minor() == _["Monero"]["from"]["minor"]
    assert derivation.major() == _["Monero"]["from"]["major"]

    derivation.clean()
    assert derivation.minor() == _["Monero"]["default"]["minor"]
    assert derivation.major() == _["Monero"]["default"]["major"]

    derivation = MoneroDerivation()
    derivation.from_minor(_["Monero"]["from"]["minor"])
    derivation.from_major(_["Monero"]["from"]["major"])
    assert derivation.minor() == _["Monero"]["from"]["minor"]
    assert derivation.major() == _["Monero"]["from"]["major"]