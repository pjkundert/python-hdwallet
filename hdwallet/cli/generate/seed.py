#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import click
import sys

from ...mnemonics import MNEMONICS
from ...seeds import (
    ISeed, BIP39Seed, CardanoSeed, ElectrumV2Seed, SEEDS
)


def generate_seed(**kwargs) -> None:
    try:
        if kwargs.get("name") not in SEEDS.keys():
            click.echo(click.style(
                f"Wrong seed name, (expected={list(SEEDS.keys())}, got='{kwargs.get('name')}')"
            ), err=True)
            sys.exit()

        mnemonic_name: str = "BIP39" if kwargs.get("name") == CardanoSeed.name() else kwargs.get("name")
        if not MNEMONICS[mnemonic_name].is_valid(mnemonic=kwargs.get("mnemonic")):
            click.echo(click.style(f"Invalid {mnemonic_name} mnemonic"), err=True)
            sys.exit()


        if kwargs.get("name") == BIP39Seed.name():
            seed: ISeed = BIP39Seed(
                seed=BIP39Seed.from_mnemonic(
                    mnemonic=kwargs.get("mnemonic"),
                    passphrase=kwargs.get("passphrase")
                )
            )
        elif kwargs.get("name") == CardanoSeed.name():
            seed: ISeed = CardanoSeed(
                seed=CardanoSeed.from_mnemonic(
                    mnemonic=kwargs.get("mnemonic"),
                    passphrase=kwargs.get("passphrase"),
                    cardano_type=kwargs.get("cardano_type")
                )
            )
        elif kwargs.get("name") == ElectrumV2Seed.name():
            seed: ISeed = ElectrumV2Seed(
                seed=ElectrumV2Seed.from_mnemonic(
                    mnemonic=kwargs.get("mnemonic"),
                    passphrase=kwargs.get("passphrase"),
                    mnemonic_type=kwargs.get("mnemonic_type")
                )
            )
        else:
            seed: ISeed = SEEDS[kwargs.get("name")].__call__(
                seed=SEEDS[kwargs.get("name")].from_mnemonic(
                    mnemonic=kwargs.get("mnemonic")
                )
            )
        output: dict = {
            "name": seed.name(),
            "seed": seed.seed()
        }
        if seed.name() == CardanoSeed.name():
            output["cardano_type"] = kwargs.get("cardano_type")
        elif seed.name() == ElectrumV2Seed.name():
            output["mnemonic_type"] = kwargs.get("mnemonic_type")
        click.echo(json.dumps(
            output, indent=kwargs.get("indent", 4), ensure_ascii=kwargs.get("ensure_ascii", False)
        ))

    except Exception as exception:
        click.echo(click.style(f"Error: {str(exception)}"), err=True)
        sys.exit()
