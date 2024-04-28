#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Type

import json
import click
import sys

from ..entropies import ENTROPIES
from ..mnemonics import MNEMONICS
from ..seeds import SEEDS
from ..hds import HDS
from ..derivations import DERIVATIONS
from ..cryptocurrencies import (
    ICryptocurrency, get_cryptocurrency
)
from ..hdwallet import HDWallet


def dump(**kwargs) -> None:
    try:
        cryptocurrency: Type[ICryptocurrency] = get_cryptocurrency(
            symbol=kwargs.get("symbol")
        )
        if not HDS.is_hd(name=kwargs.get("hd")):
            click.echo(click.style(
                f"Wrong HD name, (expected={HDS.names()}, got='{kwargs.get('hd')}')"
            ), err=True)
            sys.exit()
        if not DERIVATIONS.is_derivation(name=kwargs.get("derivation")):
            click.echo(click.style(
                f"Wrong from derivation name, (expected={DERIVATIONS.names()}, got='{kwargs.get('derivation')}')"
            ), err=True)
            sys.exit()
        if not cryptocurrency.NETWORKS.is_network(network=kwargs.get("network")):
            click.echo(click.style(
                f"Invalid {cryptocurrency.NAME} cryptocurrency network, "
                f"(expected={cryptocurrency.NETWORKS.get_networks()}, got='{kwargs.get('network')}')"
            ), err=True)
            sys.exit()

        semantic = kwargs.get("semantic")
        if semantic is None:
            if kwargs.get("hd") in [
                "BIP32", "BIP44", "BIP86", "Cardano"
            ]:
                semantic = "P2PKH"
            elif kwargs.get("hd") == "BIP49":
                semantic = "P2WPKH_IN_P2SH"
            elif kwargs.get("hd") in ["BIP84", "BIP141"]:
                semantic = "P2WPKH"

        hdwallet: HDWallet = HDWallet(
            cryptocurrency=cryptocurrency,
            hd=HDS.hd(name=kwargs.get("hd")),
            network=kwargs.get("network"),
            public_key_type=kwargs.get("public_key_type"),
            passphrase=kwargs.get("passphrase"),
            cardano_type=kwargs.get("cardano_type"),
            address_type=kwargs.get("address_type"),
            staking_public_key=kwargs.get("staking_public_key"),
            mode=kwargs.get("mode"),
            mnemonic_type=kwargs.get("mnemonic_type"),
            checksum=kwargs.get("checksum"),
            semantic=semantic
        )

        if kwargs.get("entropy"):
            if not ENTROPIES.is_entropy(name=kwargs.get("entropy_name")):
                click.echo(click.style(
                    f"Wrong entropy name, (expected={ENTROPIES.names()}, got='{kwargs.get('entropy_name')}')"
                ), err=True)
                sys.exit()
            hdwallet.from_entropy(
                entropy=ENTROPIES.entropy(name=kwargs.get("entropy_name")).__call__(
                    entropy=kwargs.get("entropy")
                )
            )
        elif kwargs.get("mnemonic"):
            if not MNEMONICS.is_mnemonic(name=kwargs.get("mnemonic_name")):
                click.echo(click.style(
                    f"Wrong mnemonic name, (expected={MNEMONICS.names()}, got='{kwargs.get('mnemonic_name')}')"
                ), err=True)
                sys.exit()
            hdwallet.from_mnemonic(
                mnemonic=MNEMONICS.mnemonic(name=kwargs.get("mnemonic_name")).__call__(
                    mnemonic=kwargs.get("mnemonic")
                )
            )
        elif kwargs.get("seed"):
            if not SEEDS.is_seed(name=kwargs.get("seed_name")):
                click.echo(click.style(
                    f"Wrong seed name, (expected={SEEDS.names()}, got='{kwargs.get('seed_name')}')"
                ), err=True)
                sys.exit()
            hdwallet.from_seed(
                seed=SEEDS.seed(name=kwargs.get("seed_name")).__call__(
                    seed=kwargs.get("seed")
                )
            )
        elif kwargs.get("xprivate_key"):
            hdwallet.from_xprivate_key(
                xprivate_key=kwargs.get("xprivate_key"),
                encoded=kwargs.get("encoded"),
                strict=kwargs.get("strict")
            )
        elif kwargs.get("xpublic_key"):
            hdwallet.from_xpublic_key(
                xpublic_key=kwargs.get("xpublic_key"),
                encoded=kwargs.get("encoded"),
                strict=kwargs.get("strict")
            )
        elif kwargs.get("private_key"):
            hdwallet.from_private_key(
                private_key=kwargs.get("private_key")
            )
        elif kwargs.get("wif"):
            hdwallet.from_wif(
                wif=kwargs.get("wif")
            )
        elif kwargs.get("public_key"):
            hdwallet.from_public_key(
                public_key=kwargs.get("public_key")
            )
        elif kwargs.get("spend_private_key"):
            hdwallet.from_spend_private_key(
                spend_private_key=kwargs.get("spend_private_key")
            )
        elif kwargs.get("view_private_key") and kwargs.get("spend_public_key"):
            hdwallet.from_watch_only(
                view_private_key=kwargs.get("view_private_key"),
                spend_public_key=kwargs.get("spend_public_key")
            )

        if (
            kwargs.get("entropy") or
            kwargs.get("mnemonic") or
            kwargs.get("seed") or
            kwargs.get("xprivate_key") or
            kwargs.get("xpublic_key") or
            (kwargs.get("private_key") and kwargs.get("hd") in ["Electrum-V1", "Monero"]) or
            (kwargs.get("wif") and kwargs.get("hd") == "Electrum-V1") or
            kwargs.get("spend_private_key") or
            (kwargs.get("view_private_key") and kwargs.get("spend_public_key"))
        ):

            if kwargs.get("derivation") in [
                "BIP44", "BIP49", "BIP84", "BIP86"
            ]:
                hdwallet.from_derivation(
                    derivation=DERIVATIONS.derivation(name=kwargs.get("derivation")).__call__(
                        coin_type=cryptocurrency.COIN_TYPE,
                        account=kwargs.get("account"),
                        change=kwargs.get("change"),
                        address=kwargs.get("address")
                    )
                )
            elif kwargs.get("derivation") == "CIP1852":
                hdwallet.from_derivation(
                    derivation=DERIVATIONS.derivation(name=kwargs.get("derivation")).__call__(
                        coin_type=cryptocurrency.COIN_TYPE,
                        account=kwargs.get("account"),
                        role=kwargs.get("role"),
                        address=kwargs.get("address")
                    )
                )
            elif kwargs.get("derivation") == "Custom":
                hdwallet.from_derivation(
                    derivation=DERIVATIONS.derivation(name=kwargs.get("derivation")).__call__(
                        path=kwargs.get("path", "m/"),
                        indexes=kwargs.get("indexes", [])
                    )
                )
            elif kwargs.get("derivation") == "Electrum":
                hdwallet.from_derivation(
                    derivation=DERIVATIONS.derivation(name=kwargs.get("derivation")).__call__(
                        change=kwargs.get("change"),
                        address=kwargs.get("address")
                    )
                )
            elif kwargs.get("derivation") == "Monero":
                hdwallet.from_derivation(
                    derivation=DERIVATIONS.derivation(name=kwargs.get("derivation")).__call__(
                        minor=kwargs.get("minor"),
                        major=kwargs.get("major")
                    )
                )

        click.echo(json.dumps(
            hdwallet.dump(exclude=set(kwargs.get("exclude").split(","))), indent=4, ensure_ascii=False
        ))

    except Exception as exception:
        click.echo(click.style(
            f"Error: {str(exception)}"
        ), err=True)
        sys.exit()
