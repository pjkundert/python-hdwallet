#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Optional

import click
import sys

from ...mnemonics import MNEMONICS
from ...seeds import SEEDS


def generate_seed(name: str, mnemonic: str, passphrase: Optional[str], **kwargs) -> None:
    try:
        if name not in SEEDS.keys():
            click.echo(click.style(
                f"Wrong seed name, (expected={list(SEEDS.keys())}, got='{name}')"
            ), err=True)
            sys.exit()

        mnemonic_name: str = "BIP39" if name == "Cardano" else name
        if not MNEMONICS[mnemonic_name].is_valid(mnemonic=mnemonic):
            click.echo(click.style(f"Invalid {mnemonic_name} mnemonic"), err=True)
            sys.exit()

        click.echo(SEEDS[name].from_mnemonic(
            mnemonic=mnemonic, passphrase=passphrase, **kwargs
        ))

    except Exception as exception:
        click.echo(click.style(f"Error: {str(exception)}"), err=True)
