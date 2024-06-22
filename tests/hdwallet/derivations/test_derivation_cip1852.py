#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import os
import pytest

from hdwallet.derivations.cip1852 import (
    CIP1852Derivation, ROLES
)
from hdwallet.exceptions import DerivationError

# Test Values
base_path: str = os.path.dirname(__file__)
file_path: str = os.path.abspath(os.path.join(base_path, "../../data/derivations.json"))
values = open(file_path, "r", encoding="utf-8")
_: dict = json.loads(values.read())
values.close()


def test_cip1852_derivation():

    assert ROLES.EXTERNAL_CHAIN == "external-chain"
    assert ROLES.INTERNAL_CHAIN == "internal-chain"

    derivation = CIP1852Derivation()
    assert derivation.name() == _["CIP1852"]["default"]["name"]
    assert derivation.purpose() == _["CIP1852"]["default"]["purpose"]
    assert derivation.coin_type() == _["CIP1852"]["default"]["coin_type"]
    assert derivation.account() == _["CIP1852"]["default"]["account"]
    assert derivation.role() == _["CIP1852"]["default"]["role"]
    assert derivation.address() == _["CIP1852"]["default"]["address"]
    assert derivation.path() == _["CIP1852"]["default"]["path"]

    derivation = CIP1852Derivation(
        coin_type=_["CIP1852"]["from"]["coin_type"],
        account=_["CIP1852"]["from"]["account"],
        role=_["CIP1852"]["from"]["role"],
        address=_["CIP1852"]["from"]["address"]
    )
    assert derivation.coin_type() == _["CIP1852"]["from"]["coin_type"]
    assert derivation.account() == _["CIP1852"]["from"]["account"]
    assert derivation.role() == _["CIP1852"]["from"]["role"]
    assert derivation.address() == _["CIP1852"]["from"]["address"]
    assert derivation.path() == _["CIP1852"]["from"]["path"]

    derivation.clean()
    assert derivation.name() == _["CIP1852"]["default"]["name"]
    assert derivation.purpose() == _["CIP1852"]["default"]["purpose"]
    assert derivation.coin_type() == _["CIP1852"]["from"]["coin_type"]
    assert derivation.account() == _["CIP1852"]["default"]["account"]
    assert derivation.role() == _["CIP1852"]["default"]["role"]
    assert derivation.address() == _["CIP1852"]["default"]["address"]

    derivation = CIP1852Derivation()
    derivation.from_coin_type(_["CIP1852"]["from"]["coin_type"])
    derivation.from_account(_["CIP1852"]["from"]["account"])
    derivation.from_role(_["CIP1852"]["from"]["role"])
    derivation.from_address(_["CIP1852"]["from"]["address"])
    assert derivation.coin_type() == _["CIP1852"]["from"]["coin_type"]
    assert derivation.account() == _["CIP1852"]["from"]["account"]
    assert derivation.role() == _["CIP1852"]["from"]["role"]
    assert derivation.address() == _["CIP1852"]["from"]["address"]
    assert derivation.path() == _["CIP1852"]["from"]["path"]

    with pytest.raises(DerivationError):
        CIP1852Derivation(role="invalid-role")

    with pytest.raises(DerivationError):
        derivation = CIP1852Derivation()
        derivation.from_role("invalid-role")
