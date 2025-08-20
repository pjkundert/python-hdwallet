#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import re
from typing import (
    Union, Dict, Iterable, List, Optional, Tuple
)

from ...entropies import (
    IEntropy, SLIP39Entropy, SLIP39_ENTROPY_STRENGTHS
)
from ...exceptions import (
    Error, EntropyError, MnemonicError, ChecksumError
)
from ...utils import (
    get_bytes,
    bytes_to_string,
)
from ..imnemonic import IMnemonic

from shamir_mnemonic import generate_mnemonics
from shamir_mnemonic.constants import MAX_SHARE_COUNT
from shamir_mnemonic.recovery import RecoveryState, Share


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
        raise ValueError( f"Impossible group specification from {group_spec!r} w/ default size {size_default!r}: {name,(require,size)!r}" )

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

            optional          sep    default comma-separated mnemonic 
         name a secret spec          group thresholds (optional if no /)
        --------------------- --- -------------------------------------- -

       "Name threshold/groups"
        ^^^^^^^^^^^^^^^^^^^^^
        - no separator or commas, must be a secret encoding specification

                                 "group1 thresh1/mnems1, g2(t2/n1) ..."
                                  ^^^^^^^^^^^^^^^^^^^^^  ^^^^^^^^^
        - commas; can't be a secret encoding spec, so must be group specs

        Name threshold/groups [;: group1 thresh1/mnems1, g2(t2/n1) ... ]
        ^^^^^^^^^^^^^^^^^^^^^     ^^^^^^^^^^^^^^^^^^^^^  ^^^^^^^^^
        - separator; must be both a secret encoding spec, and 0 or more group specs
        - spec(s) may be partial, eg. "3" (size) or "3/" (threshold
          - sensible defaults are deduced for missing specs, if possible

    {
      ("Name",(threshold/groups)): {
        "group1": (thresh1/mnems1),
        "g2":     (t2/n2),
      }
    }
       

    """
    s_match			= language_parser.RE.match(language)
    if not s_match and language.strip():
        raise ValueError( f"Invalid SLIP-39 specification: {language!r}" )


    groups			= s_match and s_match.group("groups") or ""
    groups_list			= groups.strip().split(",")
    secret			= s_match and s_match.group("secret") or ""
    s_size_default		= len(groups_list) if groups_list else None
    s_name,(s_thresh,s_size)	= group_parser(secret, size_default=s_size_default)
    groups_list		       += [''] * (s_size - len(groups_list))  # default any missing group specs

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

    return { (s_name.strip(),(s_thresh,s_size)): dict(zip(g_names,g_sizes)) }

language_parser.REQUIRED_RATIO	= 1/2
language_parser.RE		= re.compile(
    r"""
        ^
        \s*
        (?P<secret>		# Any single name and/or spec w/ no separator or comma
            (
                [\w\s]* \d* \s* /? \s* \d*
            )
        )?
        \s* [\[<{;:]? \s*	# An optional separator or bracket may appear before group spec(s)
        (?P<groups>		# The group spec(s), comma separated
            (
                [\w\s]* \d* \s* /? \s* \d*
            )
            (
                \s* ,
                [\w\s]* \d* \s* /? \s* \d*
            )*
        )?
        \s* [\]>}]? \s*		# And optionally a trailing inverse bracket
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
        SLIP39_MNEMONIC_LANGUAGES.ENGLISH
    ]
    wordlist_path: Dict[str, str] = {
        SLIP39_MNEMONIC_LANGUAGES.ENGLISH: "slip39/wordlist/english.txt",
    }


    def __init__(self, mnemonic: Union[str, List[str]], **kwargs) -> None:
        super().__init__(mnemonic, **kwargs)
        # We know that normalize has already validated _mnemonic's length
        self._words, = filter(lambda l: len(self._mnemonic) % l == 0, self.words_list)

    @classmethod
    def name(cls) -> str:
        """
        Get the name of the mnemonic class.

        :return: The name of the entropy class.
        :rtype: str
        """
        return "SLIP39"

    def mnemonic(self) -> str:
        """
        Get the mnemonic as a single string.

        SLIP-39 Mnemonics usually have multiple lines.  Iterates the _mnemonic words list by the
        computed self.words(), joining each length of words by spaces to for a line, and then joins
        by newlines.

        :return: The mnemonic as a single string joined by spaces and newlines.
        :rtype: str

        """
        mnemonic_chunks: Iterable[List[str]] = zip(*[iter(self._mnemonic)] * self._words)
        mnemonic: Iterable[str] = map(" ".join, mnemonic_chunks)
        return "\n".join(mnemonic)

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
    def encode(
        cls,
        entropy: Union[str, bytes],
        language: str,
        passphrase: str = "",
        extendable: bool = True,
        iteration_exponent: int = 1,
        tabulate: bool = False,
    ) -> str:
        """
        Encodes entropy into a mnemonic phrase.

        This method converts a given entropy value into a mnemonic phrase according to the specified
        language.

        SLIP-39 mnemonics include a password.  This is normally empty, and is not well supported
        even on Trezor devices.  It is better to use SLIP-39 to encode a BIP-39 Mnemonic's entropy
        and then (after recovering it from SLIP-39), use a BIP-39 passphrase (which is well
        supported across all devices), or use the "Passphrase Wallet" feature of your hardware wallet
        device.

        :param entropy: The entropy to encode into a mnemonic phrase.
        :type entropy: Union[str, bytes]
        :param language: The language for the mnemonic phrase.
        :type language: str
        :param passphrase: The SLIP-39 passphrase (default: "")
        :type passphrase: str

        :return: The encoded mnemonic phrase.
        :rtype: str

        """
        entropy: bytes = get_bytes(entropy, unhexlify=True)
        if not SLIP39Entropy.is_valid_bytes_strength(len(entropy)):
            raise EntropyError(
                "Wrong entropy strength", expected=SLIP39Entropy.strengths, got=(len(entropy) * 8)
            )

        ((s_name,(s_thresh,s_size)),groups), = language_parser(language).items()
        assert s_size == len(groups)
        group_mnemonics: Sequence[Sequence[str]] = generate_mnemonics(
            group_threshold = s_thresh,
            groups = groups.values(),
            master_secret = entropy,
            passphrase = passphrase.encode('UTF-8'),
            extendable = extendable,
            iteration_exponent = iteration_exponent,
        )

        return "\n".join(sum(group_mnemonics, []))


    @classmethod
    def decode(
        cls, mnemonic: str, passphrase: str = "",
    ) -> str:
        """
        Decodes a mnemonic phrase into its corresponding entropy.

        This method converts a given mnemonic phrase back into its original entropy value.  It
        verifies several internal hashes to ensure the mnemonic and decoding is valid.  However, the
        passphrase has no verification; all derived entropies are considered equivalently valid (you
        can use several passphrases to recover multiple, distinct sets of entropy.)  So, it is
        solely your responsibility to remember your correct passphrase(s).

        :param mnemonic: The mnemonic phrase to decode.
        :type mnemonic: str
        :param passphrase: The SLIP-39 passphrase (default: "")
        :type passphrase: str

        :return: The decoded entropy as a string.
        :rtype: str

        """
        mnemonic_list: List[str] = cls.normalize(mnemonic)
        mnemonic_words, = filter(lambda words: len(mnemonic_list) % words == 0, cls.words_list)
        mnemonic_chunks: Iterable[List[str]] = zip(*[iter(mnemonic_list)] * mnemonic_words)
        mnemonic: Iterable[str] = map(" ".join, mnemonic_chunks)
        recovery = RecoveryState()
        try:
            while not recovery.is_complete():
                recovery.add_share(Share.from_mnemonic(next(mnemonic)))
            return bytes_to_string(recovery.recover(passphrase.encode('UTF-8')))
        except Exception as exc:
            raise MnemonicError(f"Failed to recover SLIP-39 Mnemonics", detail=exc)


    NORMALIZE			= re.compile(
        r"""
            ^
            (
                [\w\d\s]* [^\w\d\s]	# Group 1 {
            )?
            (
                [\w\s]*			# word word ...	
            )
            $
        """, re.VERBOSE )

    
    @classmethod
    def normalize(cls, mnemonic: Union[str, List[str]]) -> List[str]:
        """Filter the supplied lines of mnemonics, rejecting groups of mnemonics not evenly divisible by
        one of the recognized SLIP-39 mnemonic lengths.

        Also accepts a single hex raw entropy value (converting it into a simple single-mnemonic
        (1/1 groups) SLIP-39 encoding).

        Filter out any prefixes consisting of word/space symbols followed by a single non-word/space
        symbol, before any number of Mnemonic word/space symbols:

                    Group  1 { word word ...
                    Group  2 ╭ word word ...
                             ╰ word word ...
                    Group  3 ┌ word word ...
                             ├ word word ...
                             └ word word ...
                    ^^^^^^^^ ^ ^^^^^^^^^^...
                           | | |
           word/digit/space* | word/space*
                             |
                  single non-word/digit/space

        """
        errors			= []
        if isinstance( mnemonic, str ):
            mnemonic_list: List[str] = []
            mnemonic_lines = filter(None, mnemonic.strip().split("\n"))

            for line_no,m in enumerate( map( cls.NORMALIZE.match, mnemonic_lines)):
                pref,mnem	= m.groups()
                if not mnem:  # Blank lines or lines without Mnemonic skipped
                    continue
                mnem		= super().normalize(mnem)
                if len(mnem) in cls.words_list:
                    mnemonic_list.extend(mnem)
                else:
                    errors.append( f"@L{line_no}; odd {len(mnem)}-word mnemonic ignored" )
        else:
            mnemonic_list: List[str] = mnemonic

        word_lengths = list(filter(lambda l: len(mnemonic_list) % l == 0, cls.words_list))
        if not word_lengths:
            errors.append( f"Mnemonics not a multiple of valid length, or a single hex entropy value" )
        if errors:
            raise MnemonicError(
                f"Invalid SLIP39 Mnemonics",
                expected=f"multiple of {', '.join(map(str, cls.words_list))}",
                got=f"{len(mnemonic_list)} total words",
                detail="; ".join(errors),
            )

        return mnemonic_list

        
        
