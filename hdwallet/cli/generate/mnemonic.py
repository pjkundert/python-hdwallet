#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Optional

import click
import sys

from ...mnemonics import (
    AlgorandMnemonic, ALGORAND_MNEMONIC_WORDS, ALGORAND_MNEMONIC_LANGUAGES,
    BIP39Mnemonic, BIP39_MNEMONIC_WORDS, BIP39_MNEMONIC_LANGUAGES,
    ElectrumV1Mnemonic, ELECTRUM_V1_MNEMONIC_WORDS, ELECTRUM_V1_MNEMONIC_LANGUAGES,
    ElectrumV2Mnemonic, ELECTRUM_V2_MNEMONIC_WORDS, ELECTRUM_V2_MNEMONIC_LANGUAGES,
    MoneroMnemonic, MONERO_MNEMONIC_WORDS, MONERO_MNEMONIC_LANGUAGES,
    MNEMONICS
)


def generate_mnemonic(name: str, language: Optional[str], entropy: Optional[str], words: Optional[str]) -> None:
    try:
        if name not in MNEMONICS.keys():
            click.echo(click.style(
                f"Wrong mnemonic name, (expected={list(MNEMONICS.keys())}, got='{name}')"
            ), err=True)
            sys.exit()

        if language is None:  # Set default language
            if name == AlgorandMnemonic.name():
                language = ALGORAND_MNEMONIC_LANGUAGES.ENGLISH
            elif name == BIP39Mnemonic.name():
                language = BIP39_MNEMONIC_LANGUAGES.ENGLISH
            elif name == ElectrumV1Mnemonic.name():
                language = ELECTRUM_V1_MNEMONIC_LANGUAGES.ENGLISH
            elif name == ElectrumV2Mnemonic.name():
                language = ELECTRUM_V2_MNEMONIC_LANGUAGES.ENGLISH
            elif name == MoneroMnemonic.name():
                language = MONERO_MNEMONIC_LANGUAGES.ENGLISH

        if words is None:  # Set default words
            if name == AlgorandMnemonic.name():
                words = ALGORAND_MNEMONIC_WORDS.TWENTY_FIVE
            elif name == BIP39Mnemonic.name():
                words = BIP39_MNEMONIC_WORDS.TWELVE
            elif name == ElectrumV1Mnemonic.name():
                words = ELECTRUM_V1_MNEMONIC_WORDS.TWELVE
            elif name == ElectrumV2Mnemonic.name():
                words = ELECTRUM_V2_MNEMONIC_WORDS.TWELVE
            elif name == MoneroMnemonic.name():
                words = MONERO_MNEMONIC_WORDS.TWELVE

        if not MNEMONICS[name].is_valid_language(language=language):
            click.echo(click.style(
                f"Wrong {name} mnemonic language, (expected={MNEMONICS[name].languages}, got='{language}')"
            ), err=True)
            sys.exit()

        if not MNEMONICS[name].is_valid_words(words=words):
            click.echo(click.style(
                f"Wrong {name} mnemonic words, (expected={MNEMONICS[name].words}, got='{words}')"
            ), err=True)
            sys.exit()

        if entropy:
            click.echo(MNEMONICS[name].from_entropy(
                entropy=entropy, language=language
            ))
        else:
            click.echo(MNEMONICS[name].from_words(
                words=words, language=language
            ))

    except Exception as exception:
        click.echo(click.style(f"Error: {str(exception)}"), err=True)
        sys.exit()
