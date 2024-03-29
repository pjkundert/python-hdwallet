#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import click
import sys

from ...entropies import ENTROPIES


def generate_entropy(name: str, strength: int) -> None:
    try:
        if name not in ENTROPIES.keys():
            click.echo(click.style(
                f"Wrong entropy name, (expected={list(ENTROPIES.keys())}, got='{name}')"
            ), err=True)
            sys.exit()

        if not ENTROPIES[name].is_valid_strength(strength=strength):
            click.echo(click.style(
                f"Wrong {name} entropy strength, (expected={ENTROPIES[name].strengths}, got='{strength}')"
            ), err=True)
            sys.exit()

        click.echo(ENTROPIES[name].generate(strength=strength))

    except Exception as exception:
        click.echo(click.style(f"Error: {str(exception)}"), err=True)
