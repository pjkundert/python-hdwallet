#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Union, Dict, List, Optional
)

import unicodedata

from ...entropies import (
    IEntropy, AlgorandEntropy, ALGORAND_ENTROPY_STRENGTHS
)
from ...crypto import sha512_256
from ...exceptions import (
    Error, EntropyError, MnemonicError
)
from ...utils import (
    get_bytes, bytes_to_string, convert_bits
)
from ..imnemonic import IMnemonic


class ALGORAND_MNEMONIC_WORDS:

    TWENTY_FIVE: int = 25


class ALGORAND_MNEMONIC_LANGUAGES:

    ENGLISH: str = "english"


class AlgorandMnemonic(IMnemonic):

    checksum_length: int = 2
    words_list: List[int] = [
        ALGORAND_MNEMONIC_WORDS.TWENTY_FIVE
    ]
    words_to_entropy_strength: Dict[int, int] = {
        ALGORAND_MNEMONIC_WORDS.TWENTY_FIVE: ALGORAND_ENTROPY_STRENGTHS.TWO_HUNDRED_FIFTY_SIX
    }
    languages: List[str] = [
        ALGORAND_MNEMONIC_LANGUAGES.ENGLISH
    ]
    wordlist_path: Dict[str, str] = {
        ALGORAND_MNEMONIC_LANGUAGES.ENGLISH: "algorand/wordlist/english.txt"
    }

    @classmethod
    def name(cls) -> str:
        return "Algorand"

    @classmethod
    def from_words(cls, words: int, language: str) -> str:
        if words not in cls.words_list:
            raise MnemonicError("Invalid mnemonic words number", expected=cls.words_list, got=words)

        return cls.from_entropy(
            entropy=AlgorandEntropy.generate(cls.words_to_entropy_strength[words]), language=language
        )

    @classmethod
    def from_entropy(cls, entropy: Union[str, bytes, IEntropy], language: str) -> str:
        if isinstance(entropy, str) or isinstance(entropy, bytes):
            return cls.encode(entropy=entropy, language=language)
        elif isinstance(entropy, AlgorandEntropy):
            return cls.encode(entropy=entropy.entropy(), language=language)
        raise EntropyError(
            "Invalid entropy instance", expected=[str, bytes, AlgorandEntropy], got=type(entropy)
        )

    @classmethod
    def encode(cls, entropy: Union[str, bytes], language: str) -> str:
        entropy: bytes = get_bytes(entropy)
        if not AlgorandEntropy.is_valid_bytes_strength(len(entropy)):
            raise EntropyError(
                "Wrong entropy strength", expected=AlgorandEntropy.strengths, got=(len(entropy) * 8)
            )

        checksum: bytes = sha512_256(entropy)[:cls.checksum_length]
        checksum_word_indexes: Optional[List[int]] = convert_bits(checksum, 8, 11)
        assert checksum_word_indexes is not None
        word_indexes: Optional[List[int]] = convert_bits(entropy, 8, 11)
        assert word_indexes is not None

        words_list: list = cls.normalize(cls.get_words_list_by_language(language=language))
        indexes: list = word_indexes + [checksum_word_indexes[0]]
        return " ".join(cls.normalize([words_list[index] for index in indexes]))

    @classmethod
    def decode(cls, mnemonic: str, **kwargs) -> str:
        words: list = cls.normalize(mnemonic)
        if len(words) not in cls.words_list:
            raise MnemonicError("Invalid mnemonic words count", expected=cls.words_list, got=len(words))

        words_list, language = cls.find_language(mnemonic=words)
        words_list_with_index: dict = {
            words_list[i]: i for i in range(len(words_list))
        }
        word_indexes = [words_list_with_index[word] for word in words]
        entropy_list: Optional[List[int]] = convert_bits(word_indexes[:-1], 11, 8)
        assert entropy_list is not None
        entropy: bytes = bytes(entropy_list)[:-1]

        checksum: bytes = sha512_256(entropy)[:cls.checksum_length]
        checksum_word_indexes: Optional[List[int]] = convert_bits(checksum, 8, 11)
        assert checksum_word_indexes is not None
        if checksum_word_indexes[0] != word_indexes[-1]:
            raise Error(
                "Invalid checksum", expected=words_list[checksum_word_indexes[0]], got=words_list[word_indexes[-1]]
            )

        return bytes_to_string(entropy)

    @classmethod
    def normalize(cls, mnemonic: Union[str, List[str]]) -> List[str]:
        mnemonic: list = mnemonic.split() if isinstance(mnemonic, str) else mnemonic
        return list(map(lambda _: unicodedata.normalize("NFKD", _.lower()), mnemonic))
