#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import os
import pytest

from hdwallet.mnemonics.algorand.mnemonic import (
    AlgorandMnemonic, ALGORAND_MNEMONIC_LANGUAGES, ALGORAND_MNEMONIC_WORDS
)
from hdwallet.exceptions import MnemonicError, EntropyError

# Test Values
base_path: str = os.path.dirname(__file__)
file_path: str = os.path.abspath(os.path.join(base_path, "../../data/mnemonics.json"))
values = open(file_path, "r", encoding="utf-8")
_: dict = json.loads(values.read())
values.close()


def test_algorand_mnemonics():
    
    assert ALGORAND_MNEMONIC_WORDS.TWENTY_FIVE == 25
    assert ALGORAND_MNEMONIC_LANGUAGES.ENGLISH == "english"

    assert AlgorandMnemonic.is_valid(mnemonic=_["Algorand"]["entropy"]["mnemonic"])
    assert AlgorandMnemonic.is_valid_language(language=_["Algorand"]["entropy"]["language"])
    assert AlgorandMnemonic.is_valid_words(words=int(_["Algorand"]["25"]["words"]))

    from_word_25 = AlgorandMnemonic.from_words(words=ALGORAND_MNEMONIC_WORDS.TWENTY_FIVE, language=ALGORAND_MNEMONIC_LANGUAGES.ENGLISH)
    assert len(from_word_25.split()) == ALGORAND_MNEMONIC_WORDS.TWENTY_FIVE
    assert AlgorandMnemonic(mnemonic=from_word_25).language().lower() == ALGORAND_MNEMONIC_LANGUAGES.ENGLISH 

    assert AlgorandMnemonic.from_entropy(entropy=_["Algorand"]["entropy"]["entropy"], language=ALGORAND_MNEMONIC_LANGUAGES.ENGLISH) == _["Algorand"]["entropy"]["mnemonic"]

    from_mnemonic = AlgorandMnemonic(mnemonic=_["Algorand"]["entropy"]["mnemonic"])
    assert from_mnemonic.name() == _["Algorand"]["entropy"]["name"]
    assert from_mnemonic.language().lower() == _["Algorand"]["entropy"]["language"]

    with pytest.raises(MnemonicError, match="Invalid mnemonic words count"): 
        AlgorandMnemonic(mnemonic="flower letter world foil coin poverty romance tongue taste hip cradle follow proud pluck ten improve")

    with pytest.raises(MnemonicError, match="Invalid mnemonic words number"):
        AlgorandMnemonic.from_words(words=100, language=ALGORAND_MNEMONIC_LANGUAGES.ENGLISH)

    with pytest.raises(EntropyError, match="Invalid entropy instance"):
        AlgorandMnemonic.from_entropy(entropy={"FAKE_ENTROPY_DICT"}, language=ALGORAND_MNEMONIC_LANGUAGES.ENGLISH)

    with pytest.raises(EntropyError, match="Wrong entropy strength"):
        AlgorandMnemonic.from_entropy(entropy="cdf694ac868efd01673fc51e897c57a0bd428503080ad4c94c7d6f6d13f095fbc8", language=ALGORAND_MNEMONIC_LANGUAGES.ENGLISH)