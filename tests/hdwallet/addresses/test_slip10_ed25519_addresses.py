#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import os
import pytest

from hdwallet.addresses.algorand import AlgorandAddress
from hdwallet.addresses.aptos import AptosAddress
from hdwallet.addresses.multiversx import MultiversXAddress
from hdwallet.addresses.near import NearAddress
from hdwallet.addresses.solana import SolanaAddress
from hdwallet.addresses.stellar import StellarAddress
from hdwallet.addresses.tezos import TezosAddress
from hdwallet.addresses.sui import SuiAddress

# Test Values
base_path: str = os.path.dirname(__file__)
file_path: str = os.path.abspath(os.path.join(base_path, "../../data/addresses.json"))
values = open(file_path, "r", encoding="utf-8")
_: dict = json.loads(values.read())
values.close()


def test_algorand_address():

    assert AlgorandAddress.name() == _["SLIP10-Ed25519"]["addresses"]["Algorand"]["name"]
    assert AlgorandAddress.encode(
        public_key=_["SLIP10-Ed25519"]["public-key"]
    ) == _["SLIP10-Ed25519"]["addresses"]["Algorand"]["encode"]

    assert AlgorandAddress.decode(
        address=_["SLIP10-Ed25519"]["addresses"]["Algorand"]["encode"]
    ) == _["SLIP10-Ed25519"]["addresses"]["Algorand"]["decode"]


def test_multiversx_address():

    assert MultiversXAddress.name() == _["SLIP10-Ed25519"]["addresses"]["MultiversX"]["name"]
    assert MultiversXAddress.encode(
        public_key=_["SLIP10-Ed25519"]["public-key"]
    ) == _["SLIP10-Ed25519"]["addresses"]["MultiversX"]["encode"]

    assert MultiversXAddress.decode(
        address=_["SLIP10-Ed25519"]["addresses"]["MultiversX"]["encode"]
    ) == _["SLIP10-Ed25519"]["addresses"]["MultiversX"]["decode"]


def test_solana_address():

    assert SolanaAddress.name() == _["SLIP10-Ed25519"]["addresses"]["Solana"]["name"]
    assert SolanaAddress.encode(
        public_key=_["SLIP10-Ed25519"]["public-key"]
    ) == _["SLIP10-Ed25519"]["addresses"]["Solana"]["encode"]

    assert SolanaAddress.decode(
        address=_["SLIP10-Ed25519"]["addresses"]["Solana"]["encode"]
    ) == _["SLIP10-Ed25519"]["addresses"]["Solana"]["decode"]


def test_stellar_address():

    assert StellarAddress.name() == _["SLIP10-Ed25519"]["addresses"]["Stellar"]["name"]
    assert StellarAddress.encode(
        public_key=_["SLIP10-Ed25519"]["public-key"]
    ) == _["SLIP10-Ed25519"]["addresses"]["Stellar"]["encode"]

    assert StellarAddress.decode(
        address=_["SLIP10-Ed25519"]["addresses"]["Stellar"]["encode"]
    ) == _["SLIP10-Ed25519"]["addresses"]["Stellar"]["decode"]


def test_tezos_address():

    assert TezosAddress.name() == _["SLIP10-Ed25519"]["addresses"]["Tezos"]["name"]
    assert TezosAddress.encode(
        public_key=_["SLIP10-Ed25519"]["public-key"]
    ) == _["SLIP10-Ed25519"]["addresses"]["Tezos"]["encode"]

    assert TezosAddress.decode(
        address=_["SLIP10-Ed25519"]["addresses"]["Tezos"]["encode"]
    ) == _["SLIP10-Ed25519"]["addresses"]["Tezos"]["decode"]


def test_sui_address():

    assert SuiAddress.name() == _["SLIP10-Ed25519"]["addresses"]["Sui"]["name"]
    assert SuiAddress.encode(
        public_key=_["SLIP10-Ed25519"]["public-key"]
    ) == _["SLIP10-Ed25519"]["addresses"]["Sui"]["encode"]

    assert SuiAddress.decode(
        address=_["SLIP10-Ed25519"]["addresses"]["Sui"]["encode"]
    ) == _["SLIP10-Ed25519"]["addresses"]["Sui"]["decode"]


def test_aptos_address():

    assert AptosAddress.name() == _["SLIP10-Ed25519"]["addresses"]["Aptos"]["name"]
    assert AptosAddress.encode(
        public_key=_["SLIP10-Ed25519"]["public-key"]
    ) == _["SLIP10-Ed25519"]["addresses"]["Aptos"]["encode"]

    assert AptosAddress.decode(
        address=_["SLIP10-Ed25519"]["addresses"]["Aptos"]["encode"]
    ) == _["SLIP10-Ed25519"]["addresses"]["Aptos"]["decode"]


def test_near_address():

    assert NearAddress.name() == _["SLIP10-Ed25519"]["addresses"]["Near"]["name"]
    assert NearAddress.encode(
        public_key=_["SLIP10-Ed25519"]["public-key"]
    ) == _["SLIP10-Ed25519"]["addresses"]["Near"]["encode"]

    assert NearAddress.decode(
        address=_["SLIP10-Ed25519"]["addresses"]["Near"]["encode"]
    ) == _["SLIP10-Ed25519"]["addresses"]["Near"]["decode"]
