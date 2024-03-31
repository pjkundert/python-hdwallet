#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Optional

import click
import sys

from ...entropies import (
    AlgorandEntropy, ALGORAND_ENTROPY_STRENGTHS,
    BIP39Entropy, BIP39_ENTROPY_STRENGTHS,
    ElectrumV1Entropy, ELECTRUM_V1_ENTROPY_STRENGTHS,
    ElectrumV2Entropy, ELECTRUM_V2_ENTROPY_STRENGTHS,
    MoneroEntropy, MONERO_ENTROPY_STRENGTHS,
    ENTROPIES
)


def generate_entropy(name: str, strength: Optional[int]) -> None:
    try:
        if name not in ENTROPIES.keys():
            click.echo(click.style(
                f"Wrong entropy name, (expected={list(ENTROPIES.keys())}, got='{name}')"
            ), err=True)
            sys.exit()

        if strength is None:  # Set default strength
            if name == AlgorandEntropy.name():
                strength = ALGORAND_ENTROPY_STRENGTHS.TWO_HUNDRED_FIFTY_SIX
            elif name == BIP39Entropy.name():
                strength = BIP39_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT
            elif name == ElectrumV1Entropy.name():
                strength = ELECTRUM_V1_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT
            elif name == ElectrumV2Entropy.name():
                strength = ELECTRUM_V2_ENTROPY_STRENGTHS.ONE_HUNDRED_THIRTY_TWO
            elif name == MoneroEntropy.name():
                strength = MONERO_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT

        if not ENTROPIES[name].is_valid_strength(strength=strength):
            click.echo(click.style(
                f"Wrong {name} entropy strength, (expected={ENTROPIES[name].strengths}, got='{strength}')"
            ), err=True)
            sys.exit()

        click.echo(ENTROPIES[name].generate(strength=strength))

    except Exception as exception:
        click.echo(click.style(f"Error: {str(exception)}"), err=True)
