#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Union, Dict, List, Optional
)

import unicodedata

from ...utils import (
    get_bytes, bytes_to_string
)
from ...crypto import sha512_256
from ...entropies.algorand import (
    AlgorandEntropy, ALGORAND_ENTROPY_LENGTHS
)
from ...utils import convert_bits
from ..imnemonic import IMnemonic


class ALGORAND_MNEMONIC_WORDS:

    TWENTY_FIVE: int = 25


class ALGORAND_MNEMONIC_LANGUAGES:

    ENGLISH: str = "english"


class AlgorandMnemonic(IMnemonic):

    checksum_length: int = 2
    words: List[int] = [
        ALGORAND_MNEMONIC_WORDS.TWENTY_FIVE
    ]
    words_to_entropy_length: Dict[int, int] = {
        ALGORAND_MNEMONIC_WORDS.TWENTY_FIVE: ALGORAND_ENTROPY_LENGTHS.TWO_HUNDRED_FIFTY_SIX
    }
    languages: List[str] = [
        ALGORAND_MNEMONIC_LANGUAGES.ENGLISH
    ]
    wordlist_path: Dict[str, str] = {
        ALGORAND_MNEMONIC_LANGUAGES.ENGLISH: "algorand/wordlist/english.txt"
    }

    @classmethod
    def from_words(cls, words: int, language: str) -> str:
        if words not in cls.words:
            raise ValueError(f"Invalid words number for mnemonic (expected {cls.words}, got {words})")

        return cls.from_entropy(
            entropy=AlgorandEntropy.generate(cls.words_to_entropy_length[words]), language=language
        )

    @classmethod
    def from_entropy(cls, entropy: Union[str, bytes], language: str) -> str:
        return cls.encode(entropy=entropy, language=language)

    @classmethod
    def encode(cls, entropy: Union[str, bytes], language: str) -> str:
        # Check entropy length
        entropy: bytes = get_bytes(entropy)
        if not AlgorandEntropy.is_valid_bytes_length(len(entropy)):
            raise ValueError(f"Wrong entropy length (expected {AlgorandEntropy.lengths}, got {len(entropy) * 8})")

        # Compute checksum word
        checksum: bytes = sha512_256(entropy)[:cls.checksum_length]
        checksum_word_indexes: Optional[List[int]] = convert_bits(checksum, 8, 11)
        # Cannot be None by converting bytes from 8-bit to 11-bit
        assert checksum_word_indexes is not None
        # Convert entropy bytes to a list of word indexes
        word_indexes: Optional[List[int]] = convert_bits(entropy, 8, 11)
        # Cannot be None by converting bytes from 8-bit to 11-bit
        assert word_indexes is not None

        words_list: list = cls.get_words_list_by_language(language=language)
        indexes: list = word_indexes + [checksum_word_indexes[0]]
        return " ".join(cls.normalize([words_list[index] for index in indexes]))

    @classmethod
    def decode(cls, mnemonic: str) -> str:
        # Check mnemonic length
        words: list = cls.normalize(mnemonic)
        if len(words) not in cls.words:
            raise ValueError(f"Invalid mnemonic words count (expected {cls.words}, got {len(words)})")

        # Detect language if it was not specified at construction
        words_list, language = cls.find_language(mnemonic=words)
        words_list_with_index: dict = {
            words_list[i]: i for i in range(len(words_list))
        }
        # Get words indexes
        word_indexes = [words_list_with_index[word] for word in words]
        # Get back entropy as list
        entropy_list: Optional[List[int]] = convert_bits(word_indexes[:-1], 11, 8)
        # Cannot be None if the number of words is valid (checked at the beginning)
        assert entropy_list is not None
        # Get back entropy bytes
        entropy: bytes = bytes(entropy_list)[:-1]

        # Validate checksum
        checksum: bytes = sha512_256(entropy)[:cls.checksum_length]
        checksum_word_indexes: Optional[List[int]] = convert_bits(checksum, 8, 11)
        # Cannot be None by converting bytes from 8-bit to 11-bit
        assert checksum_word_indexes is not None
        if checksum_word_indexes[0] != word_indexes[-1]:
            raise ValueError(
                f"Invalid checksum (expected {words_list[checksum_word_indexes[0]]}, "
                f"got {words_list[word_indexes[-1]]})"
            )

        return bytes_to_string(entropy)

    @classmethod
    def normalize(cls, mnemonic: Union[str, List[str]]) -> List[str]:
        mnemonic: list = mnemonic.split() if isinstance(mnemonic, str) else mnemonic
        return list(map(lambda _: unicodedata.normalize("NFKD", _.lower()), mnemonic))
