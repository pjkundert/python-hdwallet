#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from .ientropy import IEntropy


class ALGORAND_ENTROPY_STRENGTHS:
    """
    Constants representing the entropy strengths for Algorand.
    """

    TWO_HUNDRED_FIFTY_SIX: int = 256


class AlgorandEntropy(IEntropy):
    """
    Uses entropy to generate a mnemonic phrase specific to Algorand,
    ensuring secure account creation with a unique checksum for
    address verification.

    Here are available Algorand entropy strengths:

    +-----------------------+-------+
    | Name                  | Value |
    +=======================+=======+
    | TWO_HUNDRED_FIFTY_SIX | 256   |
    +-----------------------+-------+
    """

    strengths = [
        ALGORAND_ENTROPY_STRENGTHS.TWO_HUNDRED_FIFTY_SIX
    ]

    @classmethod
    def name(cls) -> str:
        """
        Get the name of the entropy class.

        :return: The name of the entropy class.
        :rtype: str

        >>> from hdwallet.entropies.algorand import AlgorandEntropy
        >>> entropy: AlgorandEntropy = AlgorandEntropy(entropy="...")
        >>> entropy.name()
        "Algorand"
        """

        return "Algorand"
