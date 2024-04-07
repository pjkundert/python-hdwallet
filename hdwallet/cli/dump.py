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
from ..derivations import (
    BIP44Derivation,
    BIP49Derivation,
    BIP84Derivation,
    BIP86Derivation,
    CIP1852Derivation,
    CustomDerivation,
    ElectrumDerivation,
    MoneroDerivation,
    DERIVATIONS,
    CHANGES,
    ROLES
)
from ..cryptocurrencies import (
    ICryptocurrency, get_cryptocurrency
)
from ..hdwallet import HDWallet


def dump(**kwargs) -> None:
    # try:
        cryptocurrency: Type[ICryptocurrency] = get_cryptocurrency(
            symbol=kwargs.get("symbol")
        )
        if kwargs.get("hd") not in HDS.keys():
            click.echo(click.style(
                f"Wrong HD name, (expected={list(HDS.keys())}, got='{kwargs.get('hd')}')"
            ), err=True)
            sys.exit()
        if kwargs.get("derivation") not in DERIVATIONS.keys():
            click.echo(click.style(
                f"Wrong from derivation name, (expected={list(DERIVATIONS.keys())}, got='{kwargs.get('derivation')}')"
            ), err=True)
            sys.exit()
        if not cryptocurrency.NETWORKS.is_network(network=kwargs.get("network")):
            click.echo(click.style(
                f"Invalid {cryptocurrency.NAME} cryptocurrency network, "
                f"(expected={cryptocurrency.NETWORKS.get_networks()}, got='{kwargs.get('network')}')"
            ), err=True)
            sys.exit()

        hdwallet: HDWallet = HDWallet(
            cryptocurrency=cryptocurrency,
            hd=HDS[kwargs.get("hd")],
            network=kwargs.get("network"),
            public_key_type=kwargs.get("public_key_type"),
            passphrase=kwargs.get("passphrase"),
            cardano_type=kwargs.get("cardano_type"),
            address_type=kwargs.get("address_type"),
            staking_public_key=kwargs.get("staking_public_key"),
            mode=kwargs.get("mode"),
            mnemonic_type=kwargs.get("mnemonic_type"),
            checksum=kwargs.get("checksum"),
            semantic=kwargs.get("semantic")
        )

        if kwargs.get("entropy"):
            if kwargs.get("entropy_name") not in ENTROPIES.keys():
                click.echo(click.style(
                    f"Wrong entropy name, (expected={list(ENTROPIES.keys())}, got='{kwargs.get('entropy_name')}')"
                ), err=True)
                sys.exit()
            print(kwargs.get("entropy_name"), kwargs.get("entropy"))
            hdwallet.from_entropy(
                entropy=ENTROPIES[kwargs.get("entropy_name")].__call__(
                    entropy=kwargs.get("entropy")
                )
            )
        elif kwargs.get("mnemonic"):
            if kwargs.get("mnemonic_name") not in MNEMONICS.keys():
                click.echo(click.style(
                    f"Wrong mnemonic name, (expected={list(MNEMONICS.keys())}, got='{kwargs.get('mnemonic_name')}')"
                ), err=True)
                sys.exit()
            hdwallet.from_mnemonic(
                mnemonic=MNEMONICS[kwargs.get("mnemonic_name")].__call__(
                    mnemonic=kwargs.get("mnemonic")
                )
            )
        elif kwargs.get("seed"):
            if kwargs.get("seed_name") not in SEEDS.keys():
                click.echo(click.style(
                    f"Wrong seed name, (expected={list(SEEDS.keys())}, got='{kwargs.get('seed_name')}')"
                ), err=True)
                sys.exit()
            hdwallet.from_seed(
                seed=SEEDS[kwargs.get("seed_name")].__call__(
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
            kwargs.get("xpublic_key")
        ):

            if kwargs.get("derivation") in [
                BIP44Derivation.name(), BIP49Derivation.name(), BIP84Derivation.name(), BIP86Derivation.name()
            ]:
                if kwargs.get("change") == 0:
                    change: str = CHANGES.EXTERNAL_CHAIN
                elif kwargs.get("change") == 1:
                    change: str = CHANGES.INTERNAL_CHAIN
                else:
                    click.echo(click.style(
                        f"Wrong change index, "
                        f"(expected= 0 for external-chain | 1 for internal-chain, "
                        f"got='{kwargs.get('seed_name')}')"
                    ), err=True)
                    sys.exit()
                hdwallet.from_derivation(
                    derivation=DERIVATIONS[kwargs.get("derivation")].__call__(
                        coin_type=cryptocurrency.COIN_TYPE,
                        account=kwargs.get("account", 0),
                        change=change,
                        address=kwargs.get("address", 0)
                    )
                )
            elif kwargs.get("derivation") == CIP1852Derivation.name():
                if kwargs.get("role") == 0:
                    role: str = ROLES.EXTERNAL_CHAIN
                elif kwargs.get("role") == 1:
                    role: str = ROLES.INTERNAL_CHAIN
                elif kwargs.get("role") == 2:
                    role: str = ROLES.STAKING_KEY
                else:
                    click.echo(click.style(
                        f"Wrong role index, "
                        f"(expected= 0 for external-chain | 1 for internal-chain | 2 for staking-key, "
                        f"got='{kwargs.get('seed_name')}')"
                    ), err=True)
                    sys.exit()
                hdwallet.from_derivation(
                    derivation=DERIVATIONS[kwargs.get("derivation")].__call__(
                        coin_type=cryptocurrency.COIN_TYPE,
                        account=kwargs.get("account", 0),
                        role=role,
                        address=kwargs.get("address", 0)
                    )
                )
            elif kwargs.get("derivation") == CustomDerivation.name():
                hdwallet.from_derivation(
                    derivation=DERIVATIONS[kwargs.get("derivation")].__call__(
                        path=kwargs.get("path", "m/"),
                        indexes=kwargs.get("indexes", [])
                    )
                )
            elif kwargs.get("derivation") == ElectrumDerivation.name():
                hdwallet.from_derivation(
                    derivation=DERIVATIONS[kwargs.get("derivation")].__call__(
                        change=kwargs.get("change", 0),
                        address=kwargs.get("address", 0)
                    )
                )
            elif kwargs.get("derivation") == MoneroDerivation.name():
                hdwallet.from_derivation(
                    derivation=DERIVATIONS[kwargs.get("derivation")].__call__(
                        minor=kwargs.get("minor", 1),
                        major=kwargs.get("major", 0)
                    )
                )

        # entropy_and_mnemonic: str = "semantic,strict,"
        # seed: str = entropy_and_mnemonic + "entropy,strength,mnemonic,language,"
        # xprivate_key: str = seed.replace("strict,", "") + "passphrase,seed,"
        # xpublic_key: str = xprivate_key + "root_xprivate_key,root_private_key,xprivate_key,private_key,wif,wif_type,"
        # private_key_and_wif: str = xpublic_key.replace("private_key,wif,wif_type,", "") + (
        #     "root_xpublic_key,root_chain_code,root_public_key,strict,xprivate_key,xpublic_key,chain_code,"
        #     "depth,path,index,indexes,parent_fingerprint,"
        # )
        # public_key: str = private_key_and_wif + "private_key,wif,wif_type,"
        #
        # if kwargs.get("entropy") or kwargs.get("mnemonic"):
        #     exclude: str = entropy_and_mnemonic + kwargs.get("exclude")
        # elif kwargs.get("seed"):
        #     exclude: str = seed + kwargs.get("exclude")
        # elif kwargs.get("xprivate_key"):
        #     exclude: str = xprivate_key + kwargs.get("exclude")
        # elif kwargs.get("xpublic_key"):
        #     exclude: str = xpublic_key + kwargs.get("exclude")
        # elif kwargs.get("private_key") or kwargs.get("wif"):
        #     exclude: str = private_key_and_wif + kwargs.get("exclude")
        # elif kwargs.get("public_key"):
        #     exclude: str = public_key + kwargs.get("exclude")
        # else:
        #     exclude: str = kwargs.get("exclude")

        exclude: str = kwargs.get("exclude")

        click.echo(json.dumps(
            hdwallet.dump(exclude=set(exclude.split(","))), indent=4, ensure_ascii=False
        ))

    # except Exception as exception:
    #     click.echo(click.style(f"Error: {str(exception)}"), err=True)
    #     sys.exit()
