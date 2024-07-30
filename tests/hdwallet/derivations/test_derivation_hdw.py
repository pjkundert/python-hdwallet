#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import os
import pytest

from hdwallet.derivations.hdw import (
    HDWDerivation, ECCS
)
from hdwallet.exceptions import DerivationError


def test_bip44_derivation(data):

    assert ECCS.SLIP10_Secp256k1 == "SLIP10-Secp256k1"
    assert ECCS.SLIP10_Ed25519 == "SLIP10-Ed25519"
    assert ECCS.SLIP10_Nist256p1 == "SLIP10-Nist256p1"
    assert ECCS.KHOLAW_ED25519 == "Kholaw-Ed25519"
    assert ECCS.SLIP10_Ed25519_Blake2b == "SLIP10-Ed25519-Blake2b"
    assert ECCS.SLIP10_Ed25519_Monero == "SLIP10-Ed25519-Monero"

    derivation = HDWDerivation()
    assert derivation.name() == data["derivations"]["HDW"]["default"]["name"]
    assert derivation.account() == data["derivations"]["HDW"]["default"]["account"]
    assert derivation.ecc() == data["derivations"]["HDW"]["default"]["ecc"]
    assert derivation.address() == data["derivations"]["HDW"]["default"]["address"]
    assert derivation.path() == data["derivations"]["HDW"]["default"]["path"]

    derivation = HDWDerivation(
        account=data["derivations"]["HDW"]["from"]["account"],
        ecc=data["derivations"]["HDW"]["from"]["ecc"],
        address=data["derivations"]["HDW"]["from"]["address"]
    )
    assert derivation.account() == data["derivations"]["HDW"]["from"]["account"]
    assert derivation.ecc() == data["derivations"]["HDW"]["from"]["ecc"]
    assert derivation.address() == data["derivations"]["HDW"]["from"]["address"]
    assert derivation.path() == data["derivations"]["HDW"]["from"]["path"]

    derivation.clean()
    assert derivation.name() == data["derivations"]["HDW"]["default"]["name"]
    assert derivation.account() == data["derivations"]["HDW"]["default"]["account"]
    assert derivation.ecc() == data["derivations"]["HDW"]["default"]["ecc"]
    assert derivation.address() == data["derivations"]["HDW"]["default"]["address"]

    derivation = HDWDerivation()
    derivation.from_account(data["derivations"]["HDW"]["from"]["account"])
    derivation.from_ecc(data["derivations"]["HDW"]["from"]["ecc"])
    derivation.from_address(data["derivations"]["HDW"]["from"]["address"])
    assert derivation.account() == data["derivations"]["HDW"]["from"]["account"]
    assert derivation.ecc() == data["derivations"]["HDW"]["from"]["ecc"]
    assert derivation.address() == data["derivations"]["HDW"]["from"]["address"]
    assert derivation.path() == data["derivations"]["HDW"]["from"]["path"]

    with pytest.raises(DerivationError):
        HDWDerivation(ecc="invalid-ecc")

    with pytest.raises(DerivationError):
        derivation = HDWDerivation()
        derivation.from_ecc("invalid-ecc")
