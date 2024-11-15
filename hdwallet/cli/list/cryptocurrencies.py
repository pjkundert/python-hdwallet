#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from tabulate import tabulate

import click

from ...cryptocurrencies import CRYPTOCURRENCIES


def list_cryptocurrencies():

    documents, table, headers = [], [], [
        "Cryptocurrency", "Symbol", "Coin Type", "Networks", "ECC", "HDs", "BIP38", "Addresses"
    ]

    for cryptocurrency in CRYPTOCURRENCIES.classes():

        document: dict = {
            "name": cryptocurrency.NAME,
            "symbol": cryptocurrency.SYMBOL,
            "coin_type": cryptocurrency.COIN_TYPE,
            "networks": ", ".join(cryptocurrency.NETWORKS.get_networks()),
            "ecc": cryptocurrency.ECC.NAME,
            "hds": ", ".join(cryptocurrency.HDS.get_hds()),
            "bip38": cryptocurrency.SUPPORT_BIP38,
            "addresses": ", ".join(cryptocurrency.ADDRESSES.get_addresses()),
        }
        documents.append(document)

    for document in documents:
        table.append([
            document["name"],
            document["symbol"],
            document["coin_type"],
            document["networks"],
            document["ecc"],
            document["hds"],
            document["bip38"],
            document["addresses"]
        ])

    click.echo(tabulate(
        table,
        headers,
        colalign=(
            "left", "center", "center", "center", "center", "center", "center", "center"
        )
    ))
