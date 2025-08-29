#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from abc import (
    ABC, abstractmethod
)
from typing import (
    Union, Dict, Set, List, Tuple, Optional
)

import os
import string
import unicodedata

from collections import defaultdict

from ..exceptions import MnemonicError
from ..entropies import IEntropy


class IMnemonic(ABC):

    # The specified Mnemonic's details; including the deduced language and all of its word indices
    # for decoding, including valid abbreviations and word with/without the accents.
    _mnemonic: List[str]
    _words: int
    _language: str
    _mnemonic_type: Optional[str]
    _word_indices: Dict[str, int]

    words_list: List[int]  # The valid mnemonic length(s) available, in words
    languages: List[str]
    wordlist_path: Dict[str, str]

    def __init__(self, mnemonic: Union[str, List[str]], **kwargs) -> None:
        """
        Initialize an instance of IMnemonic with a mnemonic.

        :param mnemonic: The mnemonic to initialize with, which can be a string or a list of strings.
        :type mnemonic: Union[str, List[str]]
        :param kwargs: Additional keyword arguments.

        :return: No return
        :rtype: NoneType
        """

        self._mnemonic: List[str] = self.normalize(mnemonic)
        if not self.is_valid(self._mnemonic, **kwargs):
            raise MnemonicError("Invalid mnemonic words")
        # Attempt to unambiguously determine the Mnemonic's language using the preferred 'language'
        # optionally provided.
        self._word_indices, self._language = self.find_language(self._mnemonic, language=kwargs.get("language"))
        self._mnemonic_type = kwargs.get("mnemonic_type", None)
        self._words = len(self._mnemonic)

    @classmethod
    def name(cls) -> str:
        pass

    def mnemonic(self) -> str:
        """
        Get the mnemonic as a single string.

        :return: The mnemonic as a single string joined by spaces.
        :rtype: str
        """

        return " ".join(self._mnemonic)

    def mnemonic_type(self) -> str:
        """
        Retrieves the type of the mnemonic.

        :return: The type of the mnemonic.
        :rtype: str
        """

        raise NotImplementedError

    def language(self) -> str:
        """
        Get the formatted language value.

        :return: The formatted language string where each part is capitalized.
        :rtype: str
        """
        return self._language

    def words(self) -> int:
        """
        :return: The words.
        :rtype: int
        """

        return self._words

    @classmethod
    @abstractmethod
    def from_words(cls, words: int, language: str) -> str:
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
        """Retrieves the standardized (NFC normalized, lower-cased) word list for the specified language.

        Uses NFC normalization for internal processing consistency. BIP-39 wordlists are stored in NFD
        format but we normalize to NFC for internal word comparisons and lookups.

        We do not want to use 'normalize' to do this, because normalization of Mnemonics may have
        additional functionality beyond just ensuring symbol and case standardization.

        :param language: The language for which to get the word list.
        :type language: str
        :param wordlist_path: Optional dictionary mapping language names to file paths of their word lists.
        :type wordlist_path: Optional[Dict[str, str]]

        :return: A list of words for the specified language, normalized to NFC form.
        :rtype: List[str]

        """

        wordlist_path = cls.wordlist_path if wordlist_path is None else wordlist_path
        with open(os.path.join(os.path.dirname(__file__), wordlist_path[language]), "r", encoding="utf-8") as fin:
            words_list: List[str] = [
                unicodedata.normalize("NFC", word.lower())
                for word in map(str.strip, fin.readlines())
                if word and not word.startswith("#")
            ]
        return words_list

    @classmethod
    def all_wordslist_indices(
        cls, wordlist_path: Optional[Dict[str, str]] = None
    ) -> Tuple[str, List[str], Dict[str, int]]:
        """Yields each 'candidate' language, its NFKC-normalized 'words_list', and its
        'word_indices' dict including optional accents and all unique abbreviations.

        """
        def abbreviated_indices( word_indices ):
            """We will support all unambiguous abbreviations; even down to less than 4 characters
            (the typically guaranteed /minimum/ unambiguous word size in most Mnemonic encodings.)
            This is because Mnemonic inputs often support the absolute minimum input required to
            uniquely identify a mnemonic word in a specified language.

            """
            def min_disambiguating_length(word1: str, word2: str):
                """Find the minimum length needed to disambiguate word1 from word2.  Since the words
                cannot be the same, they must differ at a valid index, or one must be longer, so the
                resultant index is always a valid index into at least the longer of the two words.

                """
                assert word1 != word2, \
                    f"Cannot disambiguate empty or identical words"
                for j in range(min(len(word1), len(word2))):
                    if word1[j] != word2[j]:
                        return j + 1
                # One is a prefix of the other; first non-prefix character disambiguates
                return j + 1

            words_sorted = sorted( word_indices )

            pair_disambiguation = list(
                min_disambiguating_length( w1, w2 )
                for w1, w2 in zip( words_sorted[0:], words_sorted[1:] )
            )
            for i in range( len( words_sorted ) - 2 ):
                beg = min(
                    pair_disambiguation[i-1 if i > 0 else i],
                    pair_disambiguation[i],
                    pair_disambiguation[i+1]
                )
                end = min(
                    len( words_sorted[i-1 if i > 0 else i] ),
                    len( words_sorted[i] ),
                    len( words_sorted[i+1] )
                )
                for length in range( beg, end - 1):
                    abbrev = words_sorted[i][:length]
                    assert abbrev not in words_sorted, \
                        f"Found {abbrev} in {words_sorted!r}"
                    yield abbrev, word_indices[words_sorted[i]]

        for candidate in wordlist_path.keys() if wordlist_path else cls.languages:
            # Normalized NFC, so characters and accents are combined
            words_list: List[str] = cls.get_words_list_by_language(
                language=candidate, wordlist_path=wordlist_path
            )
            word_indices: Dict[str,int] = {
                words_list[i]: i for i in range(len( words_list ))
            }

            def unmark( word_composed ):
                """This word may contain composite characters with accents like "é" that decompose "e
                + '".  Most mnemonic encodings require that mnemonic words without accents match
                the accented word.  Remove the non-character symbols."""
                return ''.join(
                    c
                    for c in unicodedata.normalize( "NFD", word_composed )
                    if not unicodedata.category( c ).startswith('M')
                )

            word_indices_unmarked = {
                unmark( word_composed ): i
                for word_composed, i in word_indices.items()
            }
            word_indices.update( word_indices_unmarked )

            word_indices_abbreviated = dict( abbreviated_indices( word_indices ))
            word_indices.update( word_indices_abbreviated )

            yield candidate, words_list, word_indices

    @classmethod
    def find_language(
            cls,
            mnemonic: List[str],
            wordlist_path: Optional[Dict[str, str]] = None,
            language: Optional[str] = None,
    ) -> Tuple[Dict[str, int], str]:
        """Finds the language of the given mnemonic by checking against available word list(s),
        preferring the specified 'language' if one is supplied.  If a 'wordlist_path' dict of
        {language: path} is supplied, its languages are used.  If a 'language' (optional) is
        supplied, any ambiguity is resolved by selecting the preferred language, if available and
        the mnemonic matches.  If not, the least ambiguous language found is selected.

        If an abbreviation match is found, then the language with the largest total number of
        symbols matched (least ambiguity) is considered best.  This handles the (rare) case where a
        mnemonic is valid in multiple languages, either directly or as an abbreviation (or
        completely valid in both languages):

          english: abandon about   badge machine minute ozone salon science ...
          french:  abandon aboutir badge machine minute ozone salon science ...

        Clearly, it is /possible/ to specify a Mnemonic which for which it is impossible to uniquely
        determine the language!  However, this Mnemonic would probably be encoding very poor
        entropy, so is quite unlikely to occur in a Mnemonic storing true entropy.  But, it is
        certainly possible (see above).  However, especially with abbreviations, it is possible for
        this to occur.  For these Mnemonics, it is /impossible/ to know (or guess) which language
        the Mnemonic was intended to be {en,de}coded with.  Since an incorrect "guess" would lead to
        a different seed and therefore different derived wallets -- a match to multiple languages
        with the same quality and with no preferred 'language' leads to an Exception.

        Even the final word (whchi encodes some checksum bits) cannot determine the language with
        finality, because it is only a statistical checksum!  For 128-bit 12-word encodings, only 4
        bits of checksum are represented.  Therefore, there is a 1/16 chance that any entropy that
        encodes to words in both languages will *also* have the same 4 bits of checksum!  24-word
        BIP-39 Mnemonics only encode 8 bits of checksum, so 1/256 of random entropy that encodes to
        words common to both languages will pass the checksum test.

        Therefore, specifying a 'language' is necessary to eliminate the possibility of erroneously
        recognizing the wrong language for some Mnemonic, and therefore producing the wrong derived
        cryptographic keys.


        The returned Dict[str, int] contains all accepted word -> index mappings, including all
        acceptable abbreviations, with and without character accents.  This is typically the
        expected behavior for most Mnemonic encodings ('café' == 'cafe' for Mnemonic word matching).

        :param mnemonic: The mnemonic to check, represented as a list of words.
        :type mnemonic: List[str]
        :param wordlist_path: Optional dictionary mapping language names to file paths of their word lists.
        :type wordlist_path: Optional[Dict[str, str]]
        :param language: The preferred language, used if valid and mnemonic matches.
        :type mnemonic: Optional[str]

        :return: A tuple containing the language's word indices and the language name.
        :rtype: Tuple[Dict[str, int], str]

        """

        language_words_indices: Dict[str, Dict[str, int]]
        quality: Dict[str, int] = {}  # How many language symbols were matched
        for candidate, words_list, words_indices in cls.all_wordslist_indices( wordlist_path=wordlist_path ):
            language_words_indices[candidate] = words_indices
            quality[candidate] = 0
            try:
                # Check for exact matches and unique abbreviations, ensuring comparison occurs in
                # composite "NFKC" normalized characters.
                for word in mnemonic:
                    word_composed = unicodedata.normalize( "NFKC", word )
                    try:
                        words_indices[word_composed]
                        quality[candidate] += len( word_composed )
                    except KeyError as ex:
                        raise MnemonicError(f"Unable to find word {word}") from ex

                if candidate == language:
                    # All words exactly matched word with or without accents, complete or uniquely
                    # abbreviated words in the preferred language!  We're done - we don't need to
                    # test further candidate languages.
                    return words_indices, candidate

                # All words exactly matched words in this candidate language, or some words were
                # found to be unique abbreviations of words in the candidate, but it isn't the
                # preferred language (or no preferred language was specified).  Keep track of its
                # quality of match, but carry on testing other candidate languages.
            except (MnemonicError, ValueError):
                continue

        # No unambiguous match to any preferred language found.  Select the best available.  Sort by
        # the number of characters matched (more is better - less ambiguous).  This is a statistical
        # method; it is still dangerous, and we should fail instead of returning a bad guess!
        if not quality:
            raise MnemonicError(f"Unrecognized language for mnemonic '{mnemonic}'")

        (matches, candidate), *rest = sorted(( (m, c) for c, m in quality.items()), reverse=True )
        if rest and matches == rest[0][0]:
            raise MnemonicError(f"Ambiguous language for mnemonic '{mnemonic}'; specify a preferred language")

        return language_words_indices[candidate], candidate


    @classmethod
    def is_valid(cls, mnemonic: Union[str, List[str]], **kwargs) -> bool:
        """
        Checks if the given mnemonic is valid.

        :param mnemonic: The mnemonic to check.
        :type mnemonic: str
        :param kwargs: Additional keyword arguments.

        :return: True if the strength is valid, False otherwise.
        :rtype: bool
        """

        try:
            cls.decode(mnemonic=mnemonic, **kwargs)
            return True
        except (ValueError, MnemonicError):
            return False

    @classmethod
    def is_valid_language(cls, language: str) -> bool:
        """
        Checks if the given language is valid.

        :param language: The language to check.
        :type language: str

        :return: True if the strength is valid, False otherwise.
        :rtype: bool
        """

        return language in cls.languages

    @classmethod
    def is_valid_words(cls, words: int) -> bool:
        """
        Checks if the given number of words is valid.

        :param words: The number of words to check.
        :type words: int

        :return: True if the number of mnemonic words is valid, False otherwise.
        :rtype: bool
        """

        return words in cls.words_list

    @classmethod
    def normalize(cls, mnemonic: Union[str, List[str]]) -> List[str]:
        """Normalizes the given mnemonic by splitting it into a list of words if it is a string.
        Resilient to extra whitespace, compatibility characters such as full-width symbols,
        decomposed characters and accents, and down-cases uppercase symbols using NFKC
        normalization.

        Recognizes hex strings (raw entropy), and attempts to normalize them as appropriate for the
        IMnemonic-derived class using 'from_entropy'.  Thus, all IMnemonics can accept either
        mnemonic strings or raw hex-encoded entropy, if they use the IMnemonic.normalize base
        method in their derived 'decode' and 'is_valid' implementations.

        This makes sense for most Mnemonics, which produce an repeatable encoding for the same entropy;
        Mnemonics that produce different encodings will need alternative implementations.  They should
        handle raw entropy directly.

        :param mnemonic: The mnemonic value, which can be a single string of words or a list of words.
        :type mnemonic: Union[str, List[str]]

        :return: A list of words from the mnemonic, normalized for internal processing.
        :rtype: List[str]

        """
        if isinstance(mnemonic, str):
            if ( len(mnemonic.strip()) * 4 in cls.words_to_entropy_strength.values()
                 and all(c in string.hexdigits for c in mnemonic.strip())):
                mnemonic: str = cls.from_entropy(mnemonic, language="english")
            mnemonic: List[str] = mnemonic.strip().split()
        return list(unicodedata.normalize("NFKC", word.lower()) for word in mnemonic)
