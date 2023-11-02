#!/usr/bin/env python3

# Copyright © 2020-2023, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from abc import (
    ABC, abstractmethod
)
from typing import (
    Union, Dict, List, Tuple, Optional
)

import os


class IMnemonic(ABC):

    words: List[int]
    languages: List[str]
    wordlist_path: Dict[str, str]

    @classmethod
    @abstractmethod
    def encode(cls, entropy: Union[str, bytes], language: str) -> str:
        pass

    @classmethod
    @abstractmethod
    def decode(cls, mnemonic: Union[str, List[str]]) -> str:
        pass

    @classmethod
    def get_words_list_by_language(cls, language: str, wordlist_path: Optional[Dict[str, str]] = None) -> List[str]:
        wordlist_path = cls.wordlist_path if wordlist_path is None else wordlist_path
        with open(os.path.join(os.path.dirname(__file__), wordlist_path[language]), "r", encoding="utf-8") as fin:
            words_list: List[str] = [
                word.strip() for word in fin.readlines() if word.strip() != "" and not word.startswith("#")
            ]
        return words_list

    @classmethod
    def find_language(cls, mnemonic: List[str], wordlist_path: Optional[Dict[str, str]] = None) -> Union[str, Tuple[List[str], str]]:
        for language in cls.languages:
            try:
                words_list: list = cls.get_words_list_by_language(language=language, wordlist_path=wordlist_path)
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
    def is_valid(cls, mnemonic: Union[str, List[str]]) -> bool:
        try:
            cls.decode(mnemonic=mnemonic)
            return True
        except ValueError:
            return False
