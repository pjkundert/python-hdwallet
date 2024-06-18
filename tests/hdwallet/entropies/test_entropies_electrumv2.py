#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

# import json
# import os
# import pytest

# from hdwallet.entropies.electrum.v2 import (
#     ElectrumV2Entropy, ELECTRUM_V2_ENTROPY_STRENGTHS
# )
# from hdwallet.utils import get_bytes
# from hdwallet.exceptions import EntropyError

# # Test Values
# base_path: str = os.path.dirname(__file__)
# file_path: str = os.path.abspath(os.path.join(base_path, "../../data/entropies.json"))
# values = open(file_path, "r", encoding="utf-8")
# _: dict = json.loads(values.read())
# values.close()


# def test_electrum_v2_entropy():

#     assert ELECTRUM_V2_ENTROPY_STRENGTHS.ONE_HUNDRED_THIRTY_TWO == 132
#     assert ELECTRUM_V2_ENTROPY_STRENGTHS.TWO_HUNDRED_SIXTY_FOUR == 264

#     assert ElectrumV2Entropy.is_valid_strength(strength=ELECTRUM_V2_ENTROPY_STRENGTHS.ONE_HUNDRED_THIRTY_TWO)
#     assert ElectrumV2Entropy.is_valid_strength(strength=ELECTRUM_V2_ENTROPY_STRENGTHS.TWO_HUNDRED_SIXTY_FOUR)

#     assert ElectrumV2Entropy.is_valid_bytes_strength(bytes_strength=len(get_bytes(_["Electrum-V2"]["132"]["entropy"])))
#     assert ElectrumV2Entropy.is_valid_bytes_strength(bytes_strength=len(get_bytes(_["Electrum-V2"]["264"]["entropy"])))

#     assert ElectrumV2Entropy(entropy=ElectrumV2Entropy.generate(strength=ELECTRUM_V2_ENTROPY_STRENGTHS.ONE_HUNDRED_THIRTY_TWO)).strength() == 132
#     assert ElectrumV2Entropy(entropy=ElectrumV2Entropy.generate(strength=ELECTRUM_V2_ENTROPY_STRENGTHS.TWO_HUNDRED_SIXTY_FOUR)).strength() == 264

#     ev2_128 = ElectrumV2Entropy(entropy=_["Electrum-V2"]["132"]["entropy"])
#     ev2_160 = ElectrumV2Entropy(entropy=_["Electrum-V2"]["264"]["entropy"])

#     assert ev2_128.name() == _["Electrum-V2"]["132"]["name"]
#     assert ev2_160.name() == _["Electrum-V2"]["264"]["name"]

#     assert ev2_128.strength() == _["Electrum-V2"]["132"]["strength"]
#     assert ev2_160.strength() == _["Electrum-V2"]["264"]["strength"]

#     assert ev2_128.entropy() == _["Electrum-V2"]["132"]["entropy"]
#     assert ev2_160.entropy() == _["Electrum-V2"]["264"]["entropy"]

#     with pytest.raises(EntropyError, match="Invalid entropy data"):
#         ElectrumV2Entropy(entropy="INVALID_ENTROPY")

#     with pytest.raises(EntropyError, match="Unsupported entropy strength"):
#         ElectrumV2Entropy(entropy="cdf694ac868efd01673fc51e897c57a0bd428503080ad4c94c7d6f6d13f095fbc8")
