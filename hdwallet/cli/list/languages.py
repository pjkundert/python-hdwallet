#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from tabulate import tabulate

import click

from ...mnemonics import MNEMONICS


def list_languages():

    for i, mnemonic in enumerate(MNEMONICS.values()):

        languages: list = []
        for _language in mnemonic.languages:
            language: str = ""
            for index, _ in enumerate(_language.split("-")):
                language += _.title() if index == 0 else f"-{_.title()}"
            languages.append([language])

        click.echo(tabulate(
            languages,
            [
                f"{mnemonic.name()} Languages"
            ],
            tablefmt="github",
            stralign="left",
            numalign="left"
        ))
        if len(MNEMONICS.keys()) - 1 != i:
            click.echo("\n")
