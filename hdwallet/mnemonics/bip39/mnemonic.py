#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Union, Dict, List, Optional, Type
)

import unicodedata

from ...utils import (
    get_bytes,
    bytes_to_binary_string,
    bytes_to_string,
    binary_string_to_integer,
    integer_to_binary_string,
    binary_string_to_bytes
)
from ...crypto import sha256
from ...entropies import (
    IEntropy, BIP39Entropy, BIP39_ENTROPY_LENGTHS
)
from ..imnemonic import IMnemonic


class BIP39_MNEMONIC_WORDS:

    TWELVE: int = 12
    FIFTEEN: int = 15
    EIGHTEEN: int = 18
    TWENTY_ONE: int = 21
    TWENTY_FOUR: int = 24


class BIP39_MNEMONIC_LANGUAGES:

    CHINESE_SIMPLIFIED: str = "chinese-simplified"
    CHINESE_TRADITIONAL: str = "chinese-traditional"
    CZECH: str = "czech"
    ENGLISH: str = "english"
    FRENCH: str = "french"
    ITALIAN: str = "italian"
    JAPANESE: str = "japanese"
    KOREAN: str = "korean"
    PORTUGUESE: str = "portuguese"
    RUSSIAN: str = "russian"
    SPANISH: str = "spanish"
    TURKISH: str = "turkish"


class BIP39Mnemonic(IMnemonic):

    _name = "BIP39"

    word_bit_length: int = 11
    words_list_number: int = 2048
    words: List[int] = [
        BIP39_MNEMONIC_WORDS.TWELVE,
        BIP39_MNEMONIC_WORDS.FIFTEEN,
        BIP39_MNEMONIC_WORDS.EIGHTEEN,
        BIP39_MNEMONIC_WORDS.TWENTY_ONE,
        BIP39_MNEMONIC_WORDS.TWENTY_FOUR
    ]
    words_to_entropy_length: Dict[int, int] = {
        BIP39_MNEMONIC_WORDS.TWELVE: BIP39_ENTROPY_LENGTHS.ONE_HUNDRED_TWENTY_EIGHT,
        BIP39_MNEMONIC_WORDS.FIFTEEN: BIP39_ENTROPY_LENGTHS.ONE_HUNDRED_SIXTY,
        BIP39_MNEMONIC_WORDS.EIGHTEEN: BIP39_ENTROPY_LENGTHS.ONE_HUNDRED_NINETY_TWO,
        BIP39_MNEMONIC_WORDS.TWENTY_ONE: BIP39_ENTROPY_LENGTHS.TWO_HUNDRED_TWENTY_FOUR,
        BIP39_MNEMONIC_WORDS.TWENTY_FOUR: BIP39_ENTROPY_LENGTHS.TWO_HUNDRED_FIFTY_SIX
    }
    languages: List[str] = [
        BIP39_MNEMONIC_LANGUAGES.CHINESE_SIMPLIFIED,
        BIP39_MNEMONIC_LANGUAGES.CHINESE_TRADITIONAL,
        BIP39_MNEMONIC_LANGUAGES.CZECH,
        BIP39_MNEMONIC_LANGUAGES.ENGLISH,
        BIP39_MNEMONIC_LANGUAGES.FRENCH,
        BIP39_MNEMONIC_LANGUAGES.ITALIAN,
        BIP39_MNEMONIC_LANGUAGES.JAPANESE,
        BIP39_MNEMONIC_LANGUAGES.KOREAN,
        BIP39_MNEMONIC_LANGUAGES.PORTUGUESE,
        BIP39_MNEMONIC_LANGUAGES.RUSSIAN,
        BIP39_MNEMONIC_LANGUAGES.SPANISH,
        BIP39_MNEMONIC_LANGUAGES.TURKISH
    ]
    wordlist_path: Dict[str, str] = {
        BIP39_MNEMONIC_LANGUAGES.CHINESE_SIMPLIFIED: "bip39/wordlist/chinese_simplified.txt",
        BIP39_MNEMONIC_LANGUAGES.CHINESE_TRADITIONAL: "bip39/wordlist/chinese_traditional.txt",
        BIP39_MNEMONIC_LANGUAGES.CZECH: "bip39/wordlist/czech.txt",
        BIP39_MNEMONIC_LANGUAGES.ENGLISH: "bip39/wordlist/english.txt",
        BIP39_MNEMONIC_LANGUAGES.FRENCH: "bip39/wordlist/french.txt",
        BIP39_MNEMONIC_LANGUAGES.ITALIAN: "bip39/wordlist/italian.txt",
        BIP39_MNEMONIC_LANGUAGES.JAPANESE: "bip39/wordlist/japanese.txt",
        BIP39_MNEMONIC_LANGUAGES.KOREAN: "bip39/wordlist/korean.txt",
        BIP39_MNEMONIC_LANGUAGES.PORTUGUESE: "bip39/wordlist/portuguese.txt",
        BIP39_MNEMONIC_LANGUAGES.RUSSIAN: "bip39/wordlist/russian.txt",
        BIP39_MNEMONIC_LANGUAGES.SPANISH: "bip39/wordlist/spanish.txt",
        BIP39_MNEMONIC_LANGUAGES.TURKISH: "bip39/wordlist/turkish.txt"
    }

    @classmethod
    def from_words(cls, words: int, language: str) -> str:
        if words not in cls.words:
            raise ValueError(f"Invalid words number for mnemonic (expected {cls.words}, got {words})")

        return cls.from_entropy(
            entropy=BIP39Entropy.generate(cls.words_to_entropy_length[words]), language=language
        )

    @classmethod
    def from_entropy(cls, entropy: Union[str, bytes, IEntropy], language: str) -> str:
        if isinstance(entropy, str) or isinstance(entropy, bytes):
            return cls.encode(entropy=entropy, language=language)
        elif isinstance(entropy, BIP39Entropy):
            return cls.encode(entropy=entropy.entropy(), language=language)
        raise Exception("Invalid entropy, only accept str, bytes, or BIP39 entropy class")

    @classmethod
    def encode(cls, entropy: Union[str, bytes], language: str) -> str:
        # Check entropy length
        entropy: bytes = get_bytes(entropy)
        if not BIP39Entropy.is_valid_bytes_length(len(entropy)):
            raise ValueError(f"Wrong entropy length (expected {BIP39Entropy.lengths}, got {len(entropy) * 8})")

        # Convert entropy to binary string
        entropy_binary_string: str = bytes_to_binary_string(get_bytes(entropy), len(entropy) * 8)
        # Get entropy hash as binary string
        entropy_hash_binary_string: str = bytes_to_binary_string(sha256(entropy), 32 * 8)
        # Get mnemonic binary string by concatenating entropy and checksum
        mnemonic_bin: str = entropy_binary_string + entropy_hash_binary_string[:len(entropy) // 4]

        # Get mnemonic from entropy
        mnemonic: List[str] = []
        words_list: List[str] = cls.get_words_list_by_language(language=language)
        if len(words_list) != cls.words_list_number:
            raise ValueError(f"Invalid number of loaded words list (expected {cls.words_list_number}, got {len(words_list)})")

        for index in range(len(mnemonic_bin) // cls.word_bit_length):
            # Get current word index
            word_bin: str = mnemonic_bin[index * cls.word_bit_length:(index + 1) * cls.word_bit_length]
            word_index: int = binary_string_to_integer(word_bin)
            # Get word at given index
            mnemonic.append(words_list[word_index])

        return " ".join(cls.normalize(mnemonic))

    @classmethod
    def decode(
        cls, mnemonic: str, checksum: bool = False, words_list: Optional[List[str]] = None, words_list_with_index: Optional[dict] = None
    ) -> str:
        # Check mnemonic length
        words: list = cls.normalize(mnemonic)
        if len(words) not in cls.words:
            raise ValueError(f"Invalid mnemonic words count (expected {cls.words}, got {len(words)})")

        if not words_list or not words_list_with_index:
            # Detect language if it was not specified at construction
            words_list, language = cls.find_language(mnemonic=words)
            if len(words_list) != cls.words_list_number:
                raise ValueError(f"Invalid number of loaded words list (expected {cls.words_list_number}, got {len(words_list)})")
            words_list_with_index: dict = {
                words_list[i]: i for i in range(len(words_list))
            }

        if len(words_list) != cls.words_list_number:
            raise ValueError(f"Invalid number of loaded words list (expected {cls.words_list_number}, got {len(words_list)})")

        # Get back mnemonic binary string
        mnemonic_bin: str = "".join(map(
            lambda word: integer_to_binary_string(
                words_list_with_index[word], cls.word_bit_length
            ), words
        ))

        # Get checksum length
        mnemonic_bit_length: int = len(mnemonic_bin)
        checksum_length: int = mnemonic_bit_length // 33
        # Verify checksum
        checksum_bin: str = mnemonic_bin[-checksum_length:]
        # Get back entropy binary string
        entropy: bytes = binary_string_to_bytes(
            mnemonic_bin[:-checksum_length], checksum_length * 8
        )
        # Convert entropy hash to binary string
        entropy_hash_bin: str = bytes_to_binary_string(
            sha256(entropy), 32 * 8
        )
        checksum_bin_got: str = entropy_hash_bin[:checksum_length]
        if checksum_bin != checksum_bin_got:
            raise ValueError(
                f"Invalid checksum (expected {checksum_bin}, got {checksum_bin_got})"
            )

        if checksum:
            pad_bit_len: int = (
                mnemonic_bit_length
                if mnemonic_bit_length % 8 == 0 else
                mnemonic_bit_length + (8 - mnemonic_bit_length % 8)
            )
            return bytes_to_string(
                binary_string_to_bytes(mnemonic_bin, pad_bit_len // 4)
            )
        return bytes_to_string(entropy)

    @classmethod
    def is_valid(
        cls, mnemonic: Union[str, List[str]], words_list: Optional[List[str]] = None, words_list_with_index: Optional[dict] = None
    ) -> bool:
        try:
            cls.decode(mnemonic=mnemonic, words_list=words_list, words_list_with_index=words_list_with_index)
            return True
        except (ValueError, KeyError):
            return False

    @classmethod
    def normalize(cls, mnemonic: Union[str, List[str]]) -> List[str]:
        mnemonic: list = mnemonic.split() if isinstance(mnemonic, str) else mnemonic
        return list(map(lambda _: unicodedata.normalize("NFKD", _.lower()), mnemonic))
