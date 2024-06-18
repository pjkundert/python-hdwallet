#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import os
import pytest

from hdwallet.entropies.electrum.v1 import (
    ElectrumV1Entropy, ELECTRUM_V1_ENTROPY_STRENGTHS
)
from hdwallet.utils import get_bytes
from hdwallet.exceptions import EntropyError

# Test Values
base_path: str = os.path.dirname(__file__)
file_path: str = os.path.abspath(os.path.join(base_path, "../../data/entropies.json"))
values = open(file_path, "r", encoding="utf-8")
_: dict = json.loads(values.read())
values.close()

def test_electrum_v1_entropy():

    assert ELECTRUM_V1_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT == 128
    assert ElectrumV1Entropy.is_valid_strength(strength=ELECTRUM_V1_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT)
    assert ElectrumV1Entropy.is_valid_bytes_strength(bytes_strength=len(get_bytes(_["Electrum-V1"]["128"]["entropy"])))
    assert ElectrumV1Entropy(entropy=ElectrumV1Entropy.generate(strength=ELECTRUM_V1_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT)).strength() == 128

    ev1_128 = ElectrumV1Entropy(entropy=_["Electrum-V1"]["128"]["entropy"])

    assert ev1_128.name() == _["Electrum-V1"]["128"]["name"]
    assert ev1_128.strength() == _["Electrum-V1"]["128"]["strength"]
    assert ev1_128.entropy() == _["Electrum-V1"]["128"]["entropy"]

    with pytest.raises(EntropyError, match="Invalid entropy data"):
        ElectrumV1Entropy(entropy="INVALID_ENTROPY")

    with pytest.raises(EntropyError, match="Unsupported entropy strength"):
        ElectrumV1Entropy(entropy="cdf694ac868efd01673fc51e897c57a0bd428503080ad4c94c7d6f6d13f095fbc8")
