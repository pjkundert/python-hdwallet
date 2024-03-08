#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    List, Dict, Type
)

from .icryptocurrency import ICryptocurrency
from .algorand import Algorand
from .anon import Anon
from .artax import Artax
from .asiacoin import Asiacoin
from .auroracoin import Auroracoin
from .axe import Axe
from .beetlecoin import BeetleCoin
from .bitcloud import BitCloud
from .bitcoin import Bitcoin
from .bitcoincash import BitcoinCash
from .bitcoinplus import BitcoinPlus
from .bitcoinz import BitcoinZ
from .bitsend import BitSend
from .blocknode import Blocknode
from .bolivarcoin import Bolivarcoin
from .cardano import Cardano
from .edrcoin import EDRCoin
from .einsteinium import Einsteinium
from .elrond import Elrond
from .energi import Energi
from .europecoin import EuropeCoin
from .exclusivecoin import ExclusiveCoin
from .feathercoin import Feathercoin
from .flashcoin import Flashcoin
from .foxdcoin import Foxdcoin
from .insanecoin import InsaneCoin
from .jumbucks import Jumbucks
from .mazacoin import Mazacoin
from .minexcoin import Minexcoin
from .monero import Monero
from .monk import Monk
from .monkeyproject import MonkeyProject
from .multiversx import MultiversX
from .navcoin import Navcoin
from .neo import Neo
from .neoscoin import Neoscoin
from .newyorkcoin import NewYorkCoin
from .nix import NIX
from .nubits import NuBits
from .rapids import Rapids
from .reddcoin import Reddcoin
from .rubycoin import Rubycoin
from .saluscoin import Saluscoin
from .shadowcash import ShadowCash
from .smileycoin import Smileycoin
from .solana import Solana
from .stash import Stash
from .stellar import Stellar
from .sugarchain import Sugarchain
from .tezos import Tezos
from .verge import Verge
from .viacoin import Viacoin
from .vpncoin import VPNCoin
from .whitecoin import Whitecoin
from .xuez import XUEZ
from .ycash import Ycash
from .zcash import Zcash


CRYPTOCURRENCIES: Dict[str, Type[ICryptocurrency]] = {
    "Anon": Anon,
    "Algorand": Algorand,
    "Artax": Artax,
    "Asiacoin": Asiacoin,
    "Auroracoin": Auroracoin,
    "Axe": Axe,
    "Beetle Coin": BeetleCoin,
    "Bit Cloud": BitCloud,
    "Bitcoin": Bitcoin,
    "Bitcoin Cash": BitcoinCash,
    "Bitcoin Plus": BitcoinPlus,
    "BitcoinZ": BitcoinZ,
    "Bit Send": BitSend,
    "Blocknode": Blocknode,
    "Bolivarcoin": Bolivarcoin,
    "Cardano": Cardano,
    "EDR Coin": EDRCoin,
    "Einsteinium": Einsteinium,
    "Elrond": Elrond,
    "Energi": Energi,
    "Europe Coin": EuropeCoin,
    "Exclusive Coin": ExclusiveCoin,
    "Feathercoin": Feathercoin,
    "Flashcoin": Flashcoin,
    "Foxdcoin": Foxdcoin,
    "InsaneCoin": InsaneCoin,
    "Jumbucks": Jumbucks,
    "Mazacoin": Mazacoin,
    "Minexcoin": Minexcoin,
    "Monero": Monero,
    "Monk": Monk,
    "Monkey Project": MonkeyProject,
    "MultiversX": MultiversX,
    "Navcoin": Navcoin,
    "Neo": Neo,
    "Neoscoin": Neoscoin,
    "NewYorkCoin": NewYorkCoin,
    "NIX": NIX,
    "NuBits": NuBits,
    "Rapids": Rapids,
    "Reddcoin": Reddcoin,
    "Rubycoin": Rubycoin,
    "Saluscoin": Saluscoin,
    "Shadow Cash": ShadowCash,
    "Smileycoin": Smileycoin,
    "Solana": Solana,
    "Stash": Stash,
    "Stellar": Stellar,
    "Sugarchain": Sugarchain,
    "Tezos": Tezos,
    "Verge": Verge,
    "Viacoin": Viacoin,
    "Virtual Cash": VPNCoin,
    "Whitecoin": Whitecoin,
    "XUEZ": XUEZ,
    "Ycash": Ycash,
    "Zcash": Zcash
}

__all__: List[str] = CRYPTOCURRENCIES.keys()
