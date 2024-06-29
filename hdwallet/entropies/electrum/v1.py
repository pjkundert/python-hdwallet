#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from ..ientropy import IEntropy


class ELECTRUM_V1_ENTROPY_STRENGTHS:

    ONE_HUNDRED_TWENTY_EIGHT: int = 128


class ElectrumV1Entropy(IEntropy):
    """
    Relied on user input and simple entropy to generate a seed. It did not use a
    standardized mnemonic, leading to less secure key generation.

    Here are available Electrum-V1 entropy strengths:

    +--------------------------+-------+
    | Name                     | Value |
    +==========================+=======+
    | ONE_HUNDRED_TWENTY_EIGHT |  128  |
    +--------------------------+-------+
    """

    strengths = [
        ELECTRUM_V1_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT
    ]

    @classmethod
    def name(cls) -> str:
        """
        Get the name of the entropy class.

        :return: The name of the entropy class.
        :rtype: str
        """

        return "Electrum-V1"
