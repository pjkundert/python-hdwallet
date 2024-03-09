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
from .argoneum import Argoneum
from .artax import Artax
from .aryacoin import Aryacoin
from .asiacoin import Asiacoin
from .atom import Atom
from .auroracoin import Auroracoin
from .avian import Avian
from .axe import Axe
from .bata import Bata
from .beetlecoin import BeetleCoin
from .belacoin import BelaCoin
from .bitcloud import BitCloud
from .bitcoin import Bitcoin
from .bitcoincash import BitcoinCash
from .bitcoingold import BitcoinGold
from .bitcoinplus import BitcoinPlus
from .bitcoinsv import BitcoinSV
from .bitcoinz import BitcoinZ
from .bitcore import Bitcore
from .bitsend import BitSend
from .blackcoin import Blackcoin
from .blocknode import Blocknode
from .blockstamp import BlockStamp
from .bolivarcoin import Bolivarcoin
from .britcoin import BritCoin
from .canadaecoin import CanadaECoin
from .cannacoin import Cannacoin
from .cardano import Cardano
from .clams import Clams
from .clubcoin import ClubCoin
from .cpuchain import CPUChain
from .cranepay import CranePay
from .crave import Crave
from .dash import Dash
from .defcoin import Defcoin
from .denarius import Denarius
from .diamond import Diamond
from .digitalcoin import Digitalcoin
from .edrcoin import EDRCoin
from .einsteinium import Einsteinium
from .elastos import Elastos
from .elrond import Elrond
from .energi import Energi
from .europecoin import EuropeCoin
from .exclusivecoin import ExclusiveCoin
from .feathercoin import Feathercoin
from .fix import FIX
from .flashcoin import Flashcoin
from .foxdcoin import Foxdcoin
from .gcrcoin import GCRCoin
from .gobyte import GoByte
from .gridcoin import Gridcoin
from .groestlcoin import GroestlCoin
from .helleniccoin import Helleniccoin
from .hempcoin import Hempcoin
from .hush import Hush
from .insanecoin import InsaneCoin
from .ixcoin import IXCoin
from .jumbucks import Jumbucks
from .komodo import Komodo
from .lbrycredits import LBRYCredits
from .linx import Linx
from .litecoin import Litecoin
from .litecoinz import LitecoinZ
from .lkrcoin import Lkrcoin
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
from .okcash import OKCash
from .onix import Onix
from .pesobit import Pesobit
from .pinkcoin import Pinkcoin
from .poswcoin import PoSWCoin
from .projectcoin import ProjectCoin
from .qtum import Qtum
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
from .toacoin import TOACoin
from .tron import Tron
from .ultimatesecurecash import UltimateSecureCash
from .verge import Verge
from .viacoin import Viacoin
from .vpncoin import VPNCoin
from .whitecoin import Whitecoin
from .xuez import XUEZ
from .ycash import Ycash
from .zcash import Zcash

CRYPTOCURRENCIES: Dict[str, Type[ICryptocurrency]] = {
    "Algorand": Algorand,
    "Anon": Anon,
    "Argoneum": Argoneum,
    "Artax": Artax,
    "Aryacoin": Aryacoin,
    "Asiacoin": Asiacoin,
    "Atom": Atom,
    "Auroracoin": Auroracoin,
    "Avian": Avian,
    "Axe": Axe,
    "Bata": Bata,
    "Beetle Coin": BeetleCoin,
    "Bela Coin": BelaCoin,
    "Bit Cloud": BitCloud,
    "Bitcoin": Bitcoin,
    "Bitcoin Cash": BitcoinCash,
    "Bitcoin Gold": BitcoinGold,
    "Bitcoin Plus": BitcoinPlus,
    "Bitcoin SV": BitcoinSV,
    "BitcoinZ": BitcoinZ,
    "Bitcore": Bitcore,
    "Bit Send": BitSend,
    "Blackcoin": Blackcoin,
    "Blocknode": Blocknode,
    "Block Stamp": BlockStamp,
    "Bolivarcoin": Bolivarcoin,
    "Brit Coin": BritCoin,
    "Canada eCoin": CanadaECoin,
    "Cannacoin": Cannacoin,
    "Cardano": Cardano,
    "Clams": Clams,
    "Club Coin": ClubCoin,
    "CPU Chain": CPUChain,
    "Crane Pay": CranePay,
    "Crave": Crave,
    "Dash": Dash,
    "Defcoin": Defcoin,
    "Denarius": Denarius,
    "Diamond": Diamond,
    "Digitalcoin": Digitalcoin,
    "EDR Coin": EDRCoin,
    "Einsteinium": Einsteinium,
    "Elastos": Elastos,
    "Elrond": Elrond,
    "Energi": Energi,
    "Europe Coin": EuropeCoin,
    "Exclusive Coin": ExclusiveCoin,
    "Feathercoin": Feathercoin,
    "FIX": FIX,
    "Flashcoin": Flashcoin,
    "Foxdcoin": Foxdcoin,
    "GCR Coin": GCRCoin,
    "Go Byte": GoByte,
    "Gridcoin": Gridcoin,
    "Groestl Coin": GroestlCoin,
    "Helleniccoin": Helleniccoin,
    "Hempcoin": Hempcoin,
    "Hush": Hush,
    "InsaneCoin": InsaneCoin,
    "IX Coin": IXCoin,
    "Jumbucks": Jumbucks,
    "Komodo": Komodo,
    "LBRY Credits": LBRYCredits,
    "Linx": Linx,
    "Litecoin": Litecoin,
    "LitecoinZ": LitecoinZ,
    "Lkrcoin": Lkrcoin,
    "Mazacoin": Mazacoin,
    "Minexcoin": Minexcoin,
    "Monero": Monero,
    "Monk": Monk,
    "Monkey Project": MonkeyProject,
    "MultiversX": MultiversX,
    "Navcoin": Navcoin,
    "Neo": Neo,
    "Neoscoin": Neoscoin,
    "New York Coin": NewYorkCoin,
    "NIX": NIX,
    "NuBits": NuBits,
    "OK Cash": OKCash,
    "Onix": Onix,
    "Pesobit": Pesobit,
    "Pinkcoin": Pinkcoin,
    "PoSW Coin": PoSWCoin,
    "ProjectCoin": ProjectCoin,
    "Qtum": Qtum,
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
    "TOA Coin": TOACoin,
    "Tron": Tron,
    "Ultimate Secure Cash": UltimateSecureCash,
    "Verge": Verge,
    "Viacoin": Viacoin,
    "Virtual Cash": VPNCoin,
    "Whitecoin": Whitecoin,
    "XUEZ": XUEZ,
    "Ycash": Ycash,
    "Zcash": Zcash
}

__all__: List[str] = (
    ["ICryptocurrency", "CRYPTOCURRENCIES"] + [
        cryptocurrency.__name__ for cryptocurrency in CRYPTOCURRENCIES.values()
    ]
)
