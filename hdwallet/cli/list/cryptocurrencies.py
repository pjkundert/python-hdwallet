#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from tabulate import tabulate

import click

from ...cryptocurrencies import CRYPTOCURRENCIES


def list_cryptocurrencies():

    documents, table, headers = [], [], [
        "Cryptocurrency", "Symbol", "Networks", "Coin Type"
    ]

    for name, cryptocurrency in CRYPTOCURRENCIES.items():

        document: dict = {
            "name": cryptocurrency.NAME,
            "symbol": cryptocurrency.SYMBOL,
            "networks": ", ".join(cryptocurrency.NETWORKS.get_networks()),
            "coin_type": cryptocurrency.COIN_TYPE
        }
        documents.append(document)

    for document in documents:
        table.append([
            document["name"],
            document["symbol"],
            document["networks"],
            document["coin_type"]
        ])

    click.echo(tabulate(table, headers, tablefmt="github", colalign=("left", "center", "center", "right")))
