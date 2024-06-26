#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import os
import json
import pytest
import binascii

from hdwallet.addresses.cardano import CardanoAddress
from hdwallet.cryptocurrencies.cardano import Cardano

# Test Values
base_path: str = os.path.dirname(__file__)
file_path: str = os.path.abspath(os.path.join(base_path, "../../data/addresses.json"))
values = open(file_path, "r", encoding="utf-8")
_: dict = json.loads(values.read())
values.close()


def test_cardano_addresses():
    assert CardanoAddress.name() == "Cardano"


def test_cardano_byron_icarus_address():

    assert CardanoAddress.encode_byron_icarus(
        public_key=_["Kholaw-Ed25519"]["public-key"],
        chain_code=_["Kholaw-Ed25519"]["addresses"]["byron-icarus"]["args"]["chain_code"]
    ) == _["Kholaw-Ed25519"]["addresses"]["byron-icarus"]["encode"]

    assert CardanoAddress.decode_byron_icarus(
        address=_["Kholaw-Ed25519"]["addresses"]["byron-icarus"]["encode"]
    ) == _["Kholaw-Ed25519"]["addresses"]["byron-icarus"]["decode"]

    assert CardanoAddress.encode(
        encode_type=Cardano.TYPES.BYRON_ICARUS,
        public_key=_["Kholaw-Ed25519"]["public-key"],
        chain_code=_["Kholaw-Ed25519"]["addresses"]["byron-icarus"]["args"]["chain_code"]
    ) == _["Kholaw-Ed25519"]["addresses"]["byron-icarus"]["encode"]

    assert CardanoAddress.decode(
        decode_type=Cardano.TYPES.BYRON_ICARUS,
        address=_["Kholaw-Ed25519"]["addresses"]["byron-icarus"]["encode"]
    ) == _["Kholaw-Ed25519"]["addresses"]["byron-icarus"]["decode"]


def test_cardano_byron_legacy_address():

    assert CardanoAddress.encode_byron_legacy(
        public_key=_["Kholaw-Ed25519"]["public-key"],
        path=_["Kholaw-Ed25519"]["addresses"]["byron-legacy"]["args"]["path"],
        path_key=binascii.unhexlify(_["Kholaw-Ed25519"]["addresses"]["byron-legacy"]["args"]["path_key"]),
        chain_code=_["Kholaw-Ed25519"]["addresses"]["byron-legacy"]["args"]["chain_code"]
    ) == _["Kholaw-Ed25519"]["addresses"]["byron-legacy"]["encode"]

    assert CardanoAddress.decode_byron_legacy(
        address=_["Kholaw-Ed25519"]["addresses"]["byron-legacy"]["encode"]
    ) == _["Kholaw-Ed25519"]["addresses"]["byron-legacy"]["decode"]

    assert CardanoAddress.encode(
        encode_type=Cardano.TYPES.BYRON_LEGACY,
        public_key=_["Kholaw-Ed25519"]["public-key"],
        path=_["Kholaw-Ed25519"]["addresses"]["byron-legacy"]["args"]["path"],
        path_key=binascii.unhexlify(_["Kholaw-Ed25519"]["addresses"]["byron-legacy"]["args"]["path_key"]),
        chain_code=_["Kholaw-Ed25519"]["addresses"]["byron-legacy"]["args"]["chain_code"]
    ) == _["Kholaw-Ed25519"]["addresses"]["byron-legacy"]["encode"]

    assert CardanoAddress.decode(
        decode_type=Cardano.TYPES.BYRON_LEGACY,
        address=_["Kholaw-Ed25519"]["addresses"]["byron-legacy"]["encode"]
    ) == _["Kholaw-Ed25519"]["addresses"]["byron-legacy"]["decode"]


def test_cardano_shelley_address():

    assert CardanoAddress.encode_shelley(
        public_key=_["Kholaw-Ed25519"]["public-key"],
        staking_public_key=binascii.unhexlify(_["Kholaw-Ed25519"]["addresses"]["shelley"]["args"]["staking_public_key"]),
        network=_["Kholaw-Ed25519"]["addresses"]["shelley"]["args"]["network"]
    ) == _["Kholaw-Ed25519"]["addresses"]["shelley"]["encode"]

    assert CardanoAddress.decode_shelley(
        address=_["Kholaw-Ed25519"]["addresses"]["shelley"]["encode"]
    ) == _["Kholaw-Ed25519"]["addresses"]["shelley"]["decode"]

    assert CardanoAddress.encode(
        encode_type=Cardano.ADDRESS_TYPES.PAYMENT,
        public_key=_["Kholaw-Ed25519"]["public-key"],
        staking_public_key=binascii.unhexlify(_["Kholaw-Ed25519"]["addresses"]["shelley"]["args"]["staking_public_key"]),
        network=_["Kholaw-Ed25519"]["addresses"]["shelley"]["args"]["network"]
    ) == _["Kholaw-Ed25519"]["addresses"]["shelley"]["encode"]

    assert CardanoAddress.decode(
        decode_type=Cardano.ADDRESS_TYPES.PAYMENT,
        address=_["Kholaw-Ed25519"]["addresses"]["shelley"]["encode"]
    ) == _["Kholaw-Ed25519"]["addresses"]["shelley"]["decode"]

def test_cardano_shelley_staking_address():

    assert CardanoAddress.encode_shelley_staking(
        public_key=_["Kholaw-Ed25519"]["public-key"],
        network=_["Kholaw-Ed25519"]["addresses"]["shelley-staking"]["args"]["network"]
    ) == _["Kholaw-Ed25519"]["addresses"]["shelley-staking"]["encode"]

    assert CardanoAddress.decode_shelley_staking(
        address=_["Kholaw-Ed25519"]["addresses"]["shelley-staking"]["encode"]
    ) == _["Kholaw-Ed25519"]["addresses"]["shelley-staking"]["decode"]

    assert CardanoAddress.encode(
        encode_type=Cardano.ADDRESS_TYPES.STAKING,
        public_key=_["Kholaw-Ed25519"]["public-key"],
        network=_["Kholaw-Ed25519"]["addresses"]["shelley-staking"]["args"]["network"]
    ) == _["Kholaw-Ed25519"]["addresses"]["shelley-staking"]["encode"]

    assert CardanoAddress.decode(
        decode_type=Cardano.ADDRESS_TYPES.STAKING,
        address=_["Kholaw-Ed25519"]["addresses"]["shelley-staking"]["encode"]
    ) == _["Kholaw-Ed25519"]["addresses"]["shelley-staking"]["decode"]
