#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import click
import sys

from ...entropies import (
    IEntropy,
    AlgorandEntropy, ALGORAND_ENTROPY_STRENGTHS,
    BIP39Entropy, BIP39_ENTROPY_STRENGTHS,
    ElectrumV1Entropy, ELECTRUM_V1_ENTROPY_STRENGTHS,
    ElectrumV2Entropy, ELECTRUM_V2_ENTROPY_STRENGTHS,
    MoneroEntropy, MONERO_ENTROPY_STRENGTHS,
    ENTROPIES
)


def generate_entropy(**kwargs) -> None:
    try:
        if not ENTROPIES.is_entropy(name=kwargs.get("name")):
            click.echo(click.style(
                f"Wrong entropy name, (expected={ENTROPIES.names()}, got='{kwargs.get('name')}')"
            ), err=True)
            sys.exit()

        if kwargs.get("strength") is None:  # Set default strength
            if kwargs.get("name") == AlgorandEntropy.name():
                strength: int = ALGORAND_ENTROPY_STRENGTHS.TWO_HUNDRED_FIFTY_SIX
            elif kwargs.get("name") == BIP39Entropy.name():
                strength: int = BIP39_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT
            elif kwargs.get("name") == ElectrumV1Entropy.name():
                strength: int = ELECTRUM_V1_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT
            elif kwargs.get("name") == ElectrumV2Entropy.name():
                strength: int = ELECTRUM_V2_ENTROPY_STRENGTHS.ONE_HUNDRED_THIRTY_TWO
            elif kwargs.get("name") == MoneroEntropy.name():
                strength: int = MONERO_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT
        else:
            strength: int = kwargs.get("strength")

        if not ENTROPIES.entropy(name=kwargs.get("name")).is_valid_strength(strength=strength):
            click.echo(click.style(
                f"Wrong {kwargs.get('name')} entropy strength, "
                f"(expected={ENTROPIES.entropy(name=kwargs.get('name')).strengths}, got='{strength}')"
            ), err=True)
            sys.exit()

        entropy: IEntropy = ENTROPIES.entropy(name=kwargs.get("name")).__call__(
            entropy=ENTROPIES.entropy(name=kwargs.get("name")).generate(
                strength=strength
            )
        )
        click.echo(json.dumps(
            {
                "name": entropy.name(),
                "entropy": entropy.entropy(),
                "strength": entropy.strength()
            },
            indent=kwargs.get("indent", 4),
            ensure_ascii=kwargs.get("ensure_ascii", False)
        ))

    except Exception as exception:
        click.echo(click.style(f"Error: {str(exception)}"), err=True)
        sys.exit()
