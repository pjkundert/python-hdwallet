#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Dict, List, Union, Optional
)

import unicodedata

from ....utils import (
    get_bytes, integer_to_bytes, bytes_to_string, bytes_to_integer
)
from ....crypto import hmac_sha512
from ....mnemonics.bip39 import BIP39Mnemonic
from ....mnemonics.electrum.v1 import ElectrumV1Mnemonic
from ....entropies import (
    IEntropy, ElectrumV2Entropy, ELECTRUM_V2_ENTROPY_STRENGTHS
)
from ...imnemonic import IMnemonic


class ELECTRUM_V2_MNEMONIC_WORDS:

    TWELVE: int = 12
    TWENTY_FOUR: int = 24


class ELECTRUM_V2_MNEMONIC_LANGUAGES:

    CHINESE_SIMPLIFIED: str = "chinese_simplified"
    ENGLISH: str = "english"
    PORTUGUESE: str = "portuguese"
    SPANISH: str = "spanish"


class ELECTRUM_V2_MNEMONIC_TYPES:

    STANDARD: str = "standard"
    SEGWIT: str = "segwit"
    STANDARD_2FA: str = "standard-2fa"
    SEGWIT_2FA: str = "segwit-2fa"


class ElectrumV2Mnemonic(IMnemonic):

    _name = "Electrum-V2"

    word_bit_length: int = 11
    words: List[int] = [
        ELECTRUM_V2_MNEMONIC_WORDS.TWELVE,
        ELECTRUM_V2_MNEMONIC_WORDS.TWENTY_FOUR
    ]
    words_to_entropy_strength: Dict[int, int] = {
        ELECTRUM_V2_MNEMONIC_WORDS.TWELVE: ELECTRUM_V2_ENTROPY_STRENGTHS.ONE_HUNDRED_THIRTY_TWO,
        ELECTRUM_V2_MNEMONIC_WORDS.TWENTY_FOUR: ELECTRUM_V2_ENTROPY_STRENGTHS.TWO_HUNDRED_SIXTY_FOUR
    }
    languages: List[str] = [
        ELECTRUM_V2_MNEMONIC_LANGUAGES.CHINESE_SIMPLIFIED,
        ELECTRUM_V2_MNEMONIC_LANGUAGES.ENGLISH,
        ELECTRUM_V2_MNEMONIC_LANGUAGES.PORTUGUESE,
        ELECTRUM_V2_MNEMONIC_LANGUAGES.SPANISH
    ]
    wordlist_path: Dict[str, str] = {
        ELECTRUM_V2_MNEMONIC_LANGUAGES.CHINESE_SIMPLIFIED: "electrum/v2/wordlist/chinese_simplified.txt",
        ELECTRUM_V2_MNEMONIC_LANGUAGES.ENGLISH: "electrum/v2/wordlist/english.txt",
        ELECTRUM_V2_MNEMONIC_LANGUAGES.PORTUGUESE: "electrum/v2/wordlist/portuguese.txt",
        ELECTRUM_V2_MNEMONIC_LANGUAGES.SPANISH: "electrum/v2/wordlist/spanish.txt"
    }
    mnemonic_types: Dict[str, str] = {
        ELECTRUM_V2_MNEMONIC_TYPES.STANDARD: "01",
        ELECTRUM_V2_MNEMONIC_TYPES.SEGWIT: "100",
        ELECTRUM_V2_MNEMONIC_TYPES.STANDARD_2FA: "101",
        ELECTRUM_V2_MNEMONIC_TYPES.SEGWIT_2FA: "102"
    }

    @classmethod
    def from_words(cls, words: int, language: str, mnemonic_type: str = "standard") -> str:
        if words not in cls.words:
            raise ValueError(f"Invalid words number for mnemonic (expected {cls.words}, got {words})")

        return cls.from_entropy(
            entropy=ElectrumV2Entropy.generate(cls.words_to_entropy_strength[words]), language=language, mnemonic_type=mnemonic_type
        )

    @classmethod
    def from_entropy(cls, entropy: Union[str, bytes], language: str, mnemonic_type: str = "standard", max_attempts: int = 10 ** 60) -> str:

        if isinstance(entropy, str) or isinstance(entropy, bytes):
            entropy: bytes = get_bytes(entropy)
        elif isinstance(entropy, ElectrumV2Entropy):
            entropy: bytes = get_bytes(entropy.entropy())
        else:
            raise Exception("Invalid entropy, only accept str, bytes, or Electrum-V2 entropy class")

        # Do not waste time trying if the entropy bit are not enough
        if ElectrumV2Entropy.are_entropy_bits_enough(entropy):

            # Get bip39, electrum v1 and v2 global words list
            words_list: List[str] = cls.get_words_list_by_language(
                language=language, wordlist_path=cls.wordlist_path
            )
            bip39_words_list: List[str] = cls.get_words_list_by_language(
                language=language, wordlist_path=BIP39Mnemonic.wordlist_path
            )
            bip39_words_list_with_index: dict = {
                bip39_words_list[i]: i for i in range(len(bip39_words_list))
            }
            electrum_v1_words_list: List[str] = cls.get_words_list_by_language(
                language=language, wordlist_path=ElectrumV1Mnemonic.wordlist_path
            )
            electrum_v1_words_list_with_index: dict = {
                electrum_v1_words_list[i]: i for i in range(len(electrum_v1_words_list))
            }

            # Same of Electrum: increase the entropy until a valid one is found
            entropy: int = bytes_to_integer(entropy)
            for index in range(max_attempts):
                new_entropy: int = entropy + index
                try:
                    return cls.encode(
                        entropy=integer_to_bytes(new_entropy),
                        language=language,
                        mnemonic_type=mnemonic_type,
                        words_list=words_list,
                        bip39_words_list=bip39_words_list,
                        bip39_words_list_with_index=bip39_words_list_with_index,
                        electrum_v1_words_list=electrum_v1_words_list,
                        electrum_v1_words_list_with_index=electrum_v1_words_list_with_index
                    )
                except ValueError:
                    continue

        raise ValueError("Unable to generate a valid mnemonic")

    @classmethod
    def encode(
        cls,
        entropy: Union[str, bytes],
        language: str,
        mnemonic_type: str = "standard",
        words_list: Optional[List[str]] = None,
        bip39_words_list: Optional[List[str]] = None,
        bip39_words_list_with_index: Optional[dict] = None,
        electrum_v1_words_list: Optional[List[str]] = None,
        electrum_v1_words_list_with_index: Optional[dict] = None
    ) -> str:

        # Check entropy bits enough
        entropy: int = bytes_to_integer(get_bytes(entropy))
        if not ElectrumV2Entropy.are_entropy_bits_enough(entropy):
            raise ValueError("Entropy bit length is not enough for generating a valid mnemonic")

        mnemonic: List[str] = []
        if not words_list:
            words_list = cls.get_words_list_by_language(language=language)
        while entropy > 0:
            word_index: int = entropy % len(words_list)
            entropy //= len(words_list)
            mnemonic.append(words_list[word_index])

        if not cls.is_valid(
            mnemonic=mnemonic,
            mnemonic_type=mnemonic_type,
            bip39_words_list=bip39_words_list,
            bip39_words_list_with_index=bip39_words_list_with_index,
            electrum_v1_words_list=electrum_v1_words_list,
            electrum_v1_words_list_with_index=electrum_v1_words_list_with_index
        ):
            raise ValueError("Entropy bytes are not suitable for generating a valid mnemonic")

        return " ".join(cls.normalize(mnemonic))

    @classmethod
    def decode(cls, mnemonic: str, mnemonic_type: str = "standard") -> str:

        # Check mnemonic length
        words: list = cls.normalize(mnemonic)
        if len(words) not in cls.words:
            raise ValueError(f"Invalid mnemonic words count (expected {cls.words}, got {len(words)})")

        # Check mnemonic validity
        if not cls.is_valid(mnemonic, mnemonic_type=mnemonic_type):
            raise ValueError(f"Invalid {mnemonic_type} mnemonic type words")

        # Detect language if it was not specified at construction
        words_list, language = cls.find_language(mnemonic=words)
        words_list_with_index: dict = {
            words_list[i]: i for i in range(len(words_list))
        }

        # Decode words
        entropy: int = 0
        for word in reversed(words):
            entropy: int = (entropy * len(words_list)) + words_list_with_index[word]

        return bytes_to_string(integer_to_bytes(entropy))

    @classmethod
    def is_valid(
        cls,
        mnemonic: Union[str, List[str]],
        mnemonic_type: str = "standard",
        bip39_words_list: Optional[List[str]] = None,
        bip39_words_list_with_index: Optional[dict] = None,
        electrum_v1_words_list: Optional[List[str]] = None,
        electrum_v1_words_list_with_index: Optional[dict] = None
    ) -> bool:

        if BIP39Mnemonic.is_valid(
            mnemonic, words_list=bip39_words_list, words_list_with_index=bip39_words_list_with_index
        ) or ElectrumV1Mnemonic.is_valid(
            mnemonic, words_list=electrum_v1_words_list, words_list_with_index=electrum_v1_words_list_with_index
        ):
            return False
        return cls.is_type(
            mnemonic=mnemonic, mnemonic_type=mnemonic_type
        )

    @classmethod
    def is_type(cls, mnemonic: Union[str, List[str]], mnemonic_type: str = "standard") -> bool:
        return bytes_to_string(hmac_sha512(
            b"Seed version", " ".join(cls.normalize(mnemonic))
        )).startswith(
            cls.mnemonic_types[mnemonic_type]
        )

    @classmethod
    def normalize(cls, mnemonic: Union[str, List[str]]) -> List[str]:
        mnemonic: list = mnemonic.split() if isinstance(mnemonic, str) else mnemonic
        return list(map(lambda _: unicodedata.normalize("NFKD", _.lower()), mnemonic))
