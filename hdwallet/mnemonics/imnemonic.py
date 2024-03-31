#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from abc import (
    ABC, abstractmethod
)
from typing import (
    Union, Dict, List, Tuple, Optional
)

import os

from ..entropies import IEntropy


class IMnemonic(ABC):

    _mnemonic: List[str]
    _word: int
    _language: str
    _mnemonic_type: Optional[str] = None

    words: List[int]
    languages: List[str]
    wordlist_path: Dict[str, str]

    def __init__(self, mnemonic: Union[str, List[str]], **kwargs) -> None:

        self._mnemonic: List[str] = self.normalize(mnemonic)
        if not self.is_valid(self._mnemonic, **kwargs):
            raise Exception("Invalid mnemonic words")

        _, self._language = self.find_language(self._mnemonic)
        self._mnemonic_type = kwargs.get("mnemonic_type", None)
        self._word = len(self._mnemonic)

    @classmethod
    def name(cls) -> str:
        pass

    def mnemonic(self) -> str:
        return " ".join(self._mnemonic)

    def language(self) -> str:
        language: str = ""
        for index, _ in enumerate(self._language.split("-")):
            language += _.title() if index == 0 else f"-{_.title()}"
        return language

    def word(self) -> int:
        return self._word

    @classmethod
    @abstractmethod
    def from_words(cls, words: int, language: str, **kwargs) -> str:
        pass

    @classmethod
    @abstractmethod
    def from_entropy(cls, entropy: Union[str, bytes, IEntropy], language: str, **kwargs) -> str:
        pass

    @classmethod
    @abstractmethod
    def encode(cls, entropy: Union[str, bytes], language: str) -> str:
        pass

    @classmethod
    @abstractmethod
    def decode(cls, mnemonic: Union[str, List[str]], **kwargs) -> str:
        pass

    @classmethod
    def get_words_list_by_language(
        cls, language: str, wordlist_path: Optional[Dict[str, str]] = None
    ) -> List[str]:
        wordlist_path = cls.wordlist_path if wordlist_path is None else wordlist_path
        with open(os.path.join(os.path.dirname(__file__), wordlist_path[language]), "r", encoding="utf-8") as fin:
            words_list: List[str] = [
                word.strip() for word in fin.readlines() if word.strip() != "" and not word.startswith("#")
            ]
        return words_list

    @classmethod
    def find_language(
        cls, mnemonic: List[str], wordlist_path: Optional[Dict[str, str]] = None
    ) -> Union[str, Tuple[List[str], str]]:
        for language in cls.languages:
            try:
                words_list: list = cls.normalize(
                    cls.get_words_list_by_language(
                        language=language, wordlist_path=wordlist_path
                    )
                )
                words_list_with_index: dict = {
                    words_list[i]: i for i in range(len(words_list))
                }
                for word in mnemonic:
                    try:
                        words_list_with_index[word]
                    except KeyError as ex:
                        raise ValueError(f"Unable to find word {word}") from ex
                return words_list, language
            except ValueError:
                continue
        raise ValueError(f"Invalid language for mnemonic '{mnemonic}'")

    @classmethod
    def is_valid(cls, mnemonic: Union[str, List[str]], **kwargs) -> bool:
        try:
            cls.decode(mnemonic=mnemonic, **kwargs)
            return True
        except ValueError:
            return False

    @classmethod
    def is_valid_language(cls, language: str) -> bool:
        return language in cls.languages

    @classmethod
    def is_valid_words(cls, words: int) -> bool:
        return words in cls.words

    @classmethod
    def normalize(cls, mnemonic: Union[str, List[str]]) -> List[str]:
        return mnemonic.split() if isinstance(mnemonic, str) else mnemonic
