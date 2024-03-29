#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import click
import sys

from ...mnemonics import MNEMONICS


def generate_mnemonic(name: str, language: str, words: int) -> None:
    try:
        if name not in MNEMONICS.keys():
            click.echo(click.style(
                f"Wrong mnemonic name, (expected={list(MNEMONICS.keys())}, got='{name}')"
            ), err=True)
            sys.exit()

        if language not in MNEMONICS[name].languages:
            click.echo(click.style(
                f"Wrong {name} mnemonic language, (expected={MNEMONICS[name].languages}, got='{language}')"
            ), err=True)
            sys.exit()

        if words not in MNEMONICS[name].words:
            click.echo(click.style(
                f"Wrong {name} mnemonic words, (expected={MNEMONICS[name].words}, got='{words}')"
            ), err=True)
            sys.exit()

        click.echo(MNEMONICS[name].from_words(words=words, language=language))

    except Exception as exception:
        click.echo(click.style(f"Error: {str(exception)}"), err=True)
