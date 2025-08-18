#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import re
from typing import (
    Union, Dict, List, Optional, Tuple
)

from ...entropies import (
    IEntropy, SLIP39Entropy, SLIP39_ENTROPY_STRENGTHS
)
from ...exceptions import (
    Error, EntropyError, MnemonicError, ChecksumError
)
from ..imnemonic import IMnemonic

from shamir_mnemonic import split_ems, group_ems_mnemonics
from shamir_mnemonic.constants import MAX_SHARE_COUNT

class SLIP39_MNEMONIC_WORDS:

    TWENTY: int = 20
    THIRTY_THREE: int = 33
    FIFTY_NINE: int = 59


class SLIP39_MNEMONIC_LANGUAGES:

    ENGLISH: str = "english"



def group_parser( group_spec, size_default: Optional[int]=None ) -> Tuple[str,Tuple[int,int]]:
    """Parse a SLIP-39 group specification; a name up to the first digit, ( or /, then a
    threshold/count spec:

        Frens6, Frens 6, Frens(6)	- A 3/6 group (default is 1/2 of group size, rounded up)
        Frens2/6, Frens(2/6)		- A 2/6 group

    Prevents 1/N groups (use 1/1, and duplicate the mnemonic to the N participants).

    All aspects of a group specification are optional; an empty spec yields a default group.

    """
    g_match			= group_parser.RE.match( group_spec )
    if not g_match:
        raise ValueError( f"Invalid group specification: {group_spec!r}" )
    name			= g_match.group( 'name' ) or ""
    if name:
        name			= name.strip()
    size			= g_match.group( 'size' )
    require			= g_match.group( 'require' )
    if not size:
        # eg. default or inverse required/size ratio iff require provided.  Otherwise can't guess.
        if size_default:
            size		= size_default
        elif require:
            print( f"Deducing size from require {require!r}" )
            require		= int( require )
            size		= int( require / group_parser.REQUIRED_RATIO + 0.5 )
            if size == 1 or require == 1:
                size		= require
        else:
            size		= 1  # No spec, no require; default to group size of 1
    size			= int( size )
    if not require:
        # eg. 2/4, 3/5 for size producing require > 1; else, require = size (avoids 1/N groups)
        require			= int( size * group_parser.REQUIRED_RATIO + 0.5 )
        if size == 1 or require == 1:
            require		= size
    require			= int(require)
    if size < 1 or require > size or ( require == 1 and size > 1 ):
        raise ValueError( f"Impossible group specification from {group_spec!r}: {name,(require,size)!r}" )

    return name,(require,size)

group_parser.REQUIRED_RATIO	= 1/2
group_parser.RE			= re.compile( # noqa E305
    r"""
        ^
        \s*
        (?P<name> [^\d(/]+ )?
        \s*
        [(]?
        \s*
        (?:
            (?P<require> \d* )
            \s*
            [/]
        )?
        \s*
        (?:
            (?P<size> \d* )
            \s*
        )?
        [)]?
        \s*
        $
    """, re.VERBOSE )


def language_parser(language: str) -> Dict[Tuple[str,Tuple[int,int]],Dict[Union[str,int],Tuple[int,int]]]:
    """
    Parse a SLIP-39 language dialect specification.

        Name threshold/groups [;: group1 thresh1/mnems1, g2(t2/n1) ... ]
        ^^^^^^^^^^^^^^^^^^^^^     ^^^^^^^^^^^^^^^^^^^^^  ^^^^^^^^^
            optional          sep    default comma-separated mnemonic 
         name a groups spec          group thresholds (optional if no /)

    {
      ("name",(threshold/groups)): {
        "group1": (thresh1/mnems1),
        "g2":     (t2/n2),
      }
    }
       

    """
    s_match			= language_parser.RE.match(language)
    if not s_match and language.strip():
        raise ValueError( f"Invalid SLIP-39 specification: {language!r}" )

    groups_spec			= s_match and s_match.group("groups") or ",,,"
    groups_list			= groups_spec.split(",")
    secret			= s_match and s_match.group("secret") or ""
    s_size_default		= len(groups_list) if groups_list else None
    s_name,(s_thresh,s_size)	= group_parser(secret, size_default=s_size_default)
    groups_list		       += [''] * (s_size - len(groups_list))  # default any missing group specs

    print( f"Parsing {language!r} SLIP-39 spec {s_name,(s_thresh,s_size)!r} w/ groups: {groups_list!r}" )
    g_names,g_sizes		= [],[]
    for group in groups_list:
        # Default size inferred from Fibonacci sequence of mnemonics required by default
        size_default		= None if len(g_sizes) < 2 else min(
            MAX_SHARE_COUNT,
            2 * ( g_sizes[-1][0] + g_sizes[-2][0] )
        )
        g_name,g_dims		= group_parser(group, size_default=size_default)
        if not g_name:
            g_name		= len(g_sizes)
        g_names.append(g_name)
        g_sizes.append(g_dims)

    print( f"Group specs: {g_sizes!r}" )
    return { (s_name.strip(),(s_thresh,s_size)): dict(zip(g_names,g_sizes)) }

language_parser.REQUIRED_RATIO	= 1/2
language_parser.RE		= re.compile(
    r"""
        ^
        \s*
        (?:
            (?P<secret> [^\[<{;:]* )
            \s*
            [\[<{;:]
        )?
        \s*
        (?P<groups> [^\]>}]* )
        [\]>}]?
        \s*
        $
    """, re.VERBOSE)


class SLIP39Mnemonic(IMnemonic):
    """
    Implements the SLIP39 standard, allowing the creation of mnemonic phrases for
    recovering deterministic keys.

    Here are available ``SLP39_MNEMONIC_WORDS``:

    +-----------------------+----------------------+
    | Name                  | Value                |
    +=======================+======================+
    | TWENTY                | 20                   |
    +-----------------------+----------------------+
    | THIRTY_THREE          | 33                   |
    +-----------------------+----------------------+
    | FIFTY_NINE            | 59                   |
    +-----------------------+----------------------+

    Here are available ``SLIP39_MNEMONIC_LANGUAGES``:

    +-----------------------+----------------------+
    | Name                  | Value                |
    +=======================+======================+
    | ENGLISH               | english              |
    +-----------------------+----------------------+
    """

    word_bit_length: int = 10
    words_list_number: int = 1024
    words_list: List[int] = [
        SLIP39_MNEMONIC_WORDS.TWENTY,
        SLIP39_MNEMONIC_WORDS.THIRTY_THREE,
        SLIP39_MNEMONIC_WORDS.FIFTY_NINE,
    ]
    words_to_entropy_strength: Dict[int, int] = {
        SLIP39_MNEMONIC_WORDS.TWENTY: SLIP39_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT,
        SLIP39_MNEMONIC_WORDS.THIRTY_THREE: SLIP39_ENTROPY_STRENGTHS.TWO_HUNDRED_FIFTY_SIX,
        SLIP39_MNEMONIC_WORDS.FIFTY_NINE: SLIP39_ENTROPY_STRENGTHS.FIVE_HUNDRED_TWELVE,
    }
    languages: List[str] = [
    ]
    wordlist_path: Dict[str, str] = {
    }

    @classmethod
    def name(cls) -> str:
        """
        Get the name of the mnemonic class.

        :return: The name of the entropy class.
        :rtype: str
        """
        return "SLIP39"

    @classmethod
    def from_words(cls, words: int, language: str) -> str:
        """Generates a mnemonic phrase from a specified number of words.

        This method generates a mnemonic phrase based on the specified number of words and language.
        For SLIP-39, the language word dictionary is always the same (english) so is ignored (simply
        used as a label for the generated SLIP-39), but the rest of the language string specifies
        the "dialect" (threshold of groups required/generated, and the threshold of mnemonics
        required/generated in each group).

        The default is:

          - A threshold is 1/2 the specified number of groups/mnemonics (rounded up), and
          - 4 groups of 1, 1, 4 and 6 mnemonics

        All of these language specifications produce the same 2/4 group SLIP-39 encoding:

            ""
            "Johnson"
            "2: 1/1, 1/1, 2/4, 3/6"
            "Johnson 2/4: Home 1/1, Office 1/1, Fam 2/4, Frens 3/6"

        :param words: The number of words for the mnemonic phrase.
        :type words: int
        :param language: The language for the mnemonic phrase.
        :type language: str

        :return: The generated mnemonic phrase.
        :rtype: str

        """
        if words not in cls.words_list:
            raise MnemonicError("Invalid mnemonic words number", expected=cls.words_list, got=words)

        return cls.from_entropy(
            entropy=SLIP39Entropy.generate(cls.words_to_entropy_strength[words]), language=language
        )

    @classmethod
    def from_entropy(cls, entropy: Union[str, bytes, IEntropy], language: str, **kwargs) -> str:
        """
        Generates from entropy data.  Any entropy of the correct size can be encoded as SLIP-39.

        :param entropy: The entropy data used to generate the mnemonic phrase.
        :type entropy: Union[str, bytes, IEntropy]
        :param language: The language for the mnemonic phrase.
        :type language: str

        :return: The generated mnemonic phrase.
        :rtype: str
        """
        if isinstance(entropy, str) or isinstance(entropy, bytes):
            return cls.encode(entropy=entropy, language=language)
        elif isinstance(entropy, IEntropy) and entropy.strength() in SLIP39Entropy.strengths:
            return cls.encode(entropy=entropy.entropy(), language=language)
        raise EntropyError(
            "Invalid entropy instance", expected=[str, bytes,]+list(ENTROPIES.dictionary.values()), got=type(entropy)
        )

    @classmethod
    def encode(cls, entropy: Union[str, bytes], language: str) -> str:
        """
        Encodes entropy into a mnemonic phrase.

        This method converts a given entropy value into a mnemonic phrase according to the specified language.

        :param entropy: The entropy to encode into a mnemonic phrase.
        :type entropy: Union[str, bytes]
        :param language: The language for the mnemonic phrase.
        :type language: str

        :return: The encoded mnemonic phrase.
        :rtype: str
        """

        entropy: bytes = get_bytes(entropy, unhexlify=True)
        if not BIP39Entropy.is_valid_bytes_strength(len(entropy)):
            raise EntropyError(
                "Wrong entropy strength", expected=BIP39Entropy.strengths, got=(len(entropy) * 8)
            )

        entropy_binary_string: str = bytes_to_binary_string(get_bytes(entropy), len(entropy) * 8)
        entropy_hash_binary_string: str = bytes_to_binary_string(sha256(entropy), 32 * 8)
        mnemonic_bin: str = entropy_binary_string + entropy_hash_binary_string[:len(entropy) // 4]

        mnemonic: List[str] = []
        words_list: List[str] = cls.normalize(cls.get_words_list_by_language(language=language))
        if len(words_list) != cls.words_list_number:
            raise Error(
                "Invalid number of loaded words list", expected=cls.words_list_number, got=len(words_list)
            )

        for index in range(len(mnemonic_bin) // cls.word_bit_length):
            word_bin: str = mnemonic_bin[index * cls.word_bit_length:(index + 1) * cls.word_bit_length]
            word_index: int = binary_string_to_integer(word_bin)
            mnemonic.append(words_list[word_index])

        return " ".join(cls.normalize(mnemonic))

    @classmethod
    def decode(
        cls, mnemonic: str, checksum: bool = False, words_list: Optional[List[str]] = None, words_list_with_index: Optional[dict] = None
    ) -> str:
        """
        Decodes a mnemonic phrase into its corresponding entropy.

        This method converts a given mnemonic phrase back into its original entropy value.
        It also verifies the checksum to ensure the mnemonic is valid.

        :param mnemonic: The mnemonic phrase to decode.
        :type mnemonic: str
        :param checksum: Whether to include the checksum in the returned entropy.
        :type checksum: bool
        :param words_list: Optional list of words used to decode the mnemonic. If not provided, the method will use the default word list for the language detected.
        :type words_list: Optional[List[str]]
        :param words_list_with_index: Optional dictionary mapping words to their indices for decoding. If not provided, the method will use the default mapping.
        :type words_list_with_index: Optional[dict]

        :return: The decoded entropy as a string.
        :rtype: str
        """

        words: list = cls.normalize(mnemonic)
        if len(words) not in cls.words_list:
            raise MnemonicError("Invalid mnemonic words count", expected=cls.words_list, got=len(words))

        if not words_list or not words_list_with_index:
            words_list, language = cls.find_language(mnemonic=words)
            if len(words_list) != cls.words_list_number:
                raise Error(
                    "Invalid number of loaded words list", expected=cls.words_list_number, got=len(words_list)
                )
            words_list_with_index: dict = {
                words_list[i]: i for i in range(len(words_list))
            }

        if len(words_list) != cls.words_list_number:
            raise Error(
                "Invalid number of loaded words list", expected=cls.words_list_number, got=len(words_list)
            )

        mnemonic_bin: str = "".join(map(
            lambda word: integer_to_binary_string(
                words_list_with_index[word], cls.word_bit_length
            ), words
        ))

        mnemonic_bit_length: int = len(mnemonic_bin)
        checksum_length: int = mnemonic_bit_length // 33
        checksum_bin: str = mnemonic_bin[-checksum_length:]
        entropy: bytes = binary_string_to_bytes(
            mnemonic_bin[:-checksum_length], checksum_length * 8
        )
        entropy_hash_bin: str = bytes_to_binary_string(
            sha256(entropy), 32 * 8
        )
        checksum_bin_got: str = entropy_hash_bin[:checksum_length]
        if checksum_bin != checksum_bin_got:
            raise ChecksumError(
                "Invalid checksum", expected=checksum_bin, got=checksum_bin_got
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
        cls,
        mnemonic: Union[str, List[str]],
        words_list: Optional[List[str]] = None,
        words_list_with_index: Optional[dict] = None
    ) -> bool:
        """
        Validates a mnemonic phrase.

        This method checks whether the provided mnemonic phrase is valid by attempting to decode it.
        If the decoding is successful without raising any errors, the mnemonic is considered valid.

        :param mnemonic: The mnemonic phrase to validate. It can be a string or a list of words.
        :type mnemonic: Union[str, List[str]]
        :param words_list: Optional list of words to be used for validation. If not provided, the method will use the default word list.
        :type words_list: Optional[List[str]]
        :param words_list_with_index: Optional dictionary mapping words to their indices for validation. If not provided, the method will use the default mapping.
        :type words_list_with_index: Optional[dict]

        :return: True if the mnemonic phrase is valid, False otherwise.
        :rtype: bool
        """

        try:
            cls.decode(
                mnemonic=mnemonic, words_list=words_list, words_list_with_index=words_list_with_index
            )
            return True
        except (Error, KeyError):
            return False
