#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import List

# Algorand
ALGO: str = "ALGO"
# Anon
ANON: str = "ANON"
# Argoneum
AGM: str = "AGM"
# Artax
XAX: str = "XAX"
# Aryacoin
AYA: str = "AYA"
# Asiacoin
AC: str = "AC"
# Atom
ATOM: str = "ATOM"
# Auroracoin
AUR: str = "AUR"
# Avian
AVN: str = "AVN"
# Axe
AXE: str = "AXE"
# Bata
BTA: str = "BTA"
# Beetle Coin
BEET: str = "BEET"
# Bela Coin
BELA: str = "BELA"
# Bit Cloud
BTDX: str = "BTDX"
# Bitcoin
BTC: str = "BTC"
# Bitcoin Cash
BCH: str = "BCH"
# Bitcoin Gold
BTG: str = "BTG"
# Bitcoin Plus
XBC: str = "XBC"
# Bitcoin SV
BSV: str = "BSV"
# BitcoinZ
BTCZ: str = "BTCZ"
# Bitcore
BTX: str = "BTX"
# Bit Send
BSD: str = "BSD"
# Blackcoin
BLK: str = "BLK"
# Blocknode
BND: str = "BND"
# Block Stamp
BST: str = "BST"
# Bolivarcoin
BOLI: str = "BOLI"
# Brit Coin
BRIT: str = "BRIT"
# Canada eCoin
CDN: str = "CDN"
# Cannacoin
CCN: str = "CCN"
# Cardano
ADA: str = "ADA"
# Clams
CLAM: str = "CLAM"
# Club Coin
CLUB: str = "CLUB"
# Compcoin
CMP: str = "CMP"
# CPU Chain
CPU: str = "CPU"
# Crane Pay
CRP: str = "CRP"
# Crave
CRAVE: str = "CRAVE"
# Dash
DASH: str = "DASH"
# DeepOnion
ONION: str = "ONION"
# Defcoin
DFC: str = "DFC"
# Denarius
DNR: str = "DNR"
# Diamond
DMD: str = "DMD"
# Digi Byte
DGB: str = "DGB"
# Digitalcoin
DGC: str = "DGC"
# Dogecoin
DOGE: str = "DOGE"
# E-coin
ECN: str = "ECN"
# EDR Coin
EDRC: str = "EDRC"
# Einsteinium
EMC2: str = "EMC2"
# Elastos
ELA: str = "ELA"
# Elrond or MultiversX
EGLD: str = "EGLD"
# Energi
NRG: str = "NRG"
# Ethereum
ETH: str = "ETH"
# Europe Coin
ERC: str = "ERC"
# Evrmore
EVR: str = "EVR"
# Exclusive Coin
EXCL: str = "EXCL"
# Feathercoin
FTC: str = "FTC"
# Firstcoin
FRST: str = "FRST"
# FIX
FIX: str = "FIX"
# Flashcoin
FLASH: str = "FLASH"
# Flux
FLUX: str = "FLUX"
# Foxdcoin
FOXD: str = "FOXD"
# Fuji Coin
FJC: str = "FJC"
# Game Credits
GAME: str = "GAME"
# GCR Coin
GCR: str = "GCR"
# Go Byte
GBX: str = "GBX"
# Gridcoin
GRC: str = "GRC"
# Groestl Coin
GRS: str = "GRS"
# Gulden
NLG: str = "NLG"
# Helleniccoin
HNC: str = "HNC"
# Hempcoin
THC: str = "THC"
# Hush
HUSH: str = "HUSH"
# InsaneCoin
INSN: str = "INSN"
# Internet Of People
IOP: str = "IOP"
# IX Coin
IXC: str = "IXC"
# Jumbucks
JBS: str = "JBS"
# Kobocoin
KOBO: str = "KOBO"
# Komodo
KMD: str = "KMD"
# LBRY Credits
LBC: str = "LBC"
# Linx
LINX: str = "LINX"
# Litecoin
LTC: str = "LTC"
# Litecoin Cash
LCC: str = "LCC"
# LitecoinZ
LTZ: str = "LTZ"
# Lkrcoin
LKR: str = "LKR"
# Lynx
LYNX: str = "LYNX"
# Mazacoin
MZC: str = "MZC"
# Megacoin
MEC: str = "MEC"
# Minexcoin
MNX: str = "MNX"
# Monacoin
MONA: str = "MONA"
# Monero
XMR: str = "XMR"
# Monkey Project or Monk
MONK: str = "MONK"
# Myriadcoin
XMY: str = "XMY"
# Namecoin
NMC: str = "NMC"
# Navcoin
NAV: str = "NAV"
# Neblio
NEBL: str = "NEBL"
# Neo
NEO: str = "NEO"
# Neoscoin
NEOS: str = "NEOS"
# Neurocoin
NRO: str = "NRO"
# New York Coin
NYC: str = "NYC"
# NIX
NIX: str = "NIX"
# Novacoin
NVC: str = "NVC"
# NuBits
NBT: str = "NBT"
# NuShares
NSR: str = "NSR"
# OK Cash
OK: str = "OK"
# Omni
OMNI: str = "OMNI"
# Onix
ONX: str = "ONX"
# Peercoin
PPC: str = "PPC"
# Pesobit
PSB: str = "PSB"
# Phore
PHR: str = "PHR"
# Pinkcoin
PINK: str = "PINK"
# Pivx
PIVX: str = "PIVX"
# PoSW Coin
POSW: str = "POSW"
# Potcoin
POT: str = "POT"
# Project Coin
PRJ: str = "PRJ"
# Putincoin
PUT: str = "PUT"
# Qtum
QTUM: str = "QTUM"
# Rapids
RPD: str = "RPD"
# Ravencoin
RVN: str = "RVN"
# Reddcoin
RDD: str = "RDD"
# Ripple
XRP: str = "XRP"
# RSK
RBTC: str = "RBTC"
# Rubycoin
RBY: str = "RBY"
# Safecoin
SAFE: str = "SAFE"
# Saluscoin
SLS: str = "SLS"
# Scribe
SCRIBE: str = "SCRIBE"
# Shadow Cash
SDC: str = "SDC"
# Slimcoin
SLM: str = "SLM"
# Smileycoin
SMLY: str = "SMLY"
# Solana
SOL: str = "SOL"
# Solarcoin
SLR: str = "SLR"
# Stash
STASH: str = "STASH"
# Stellar
XLM: str = "XLM"
# Stratis
STRAT: str = "STRAT"
# Sugarchain
SUGAR: str = "SUGAR"
# Syscoin
SYS: str = "SYS"
# Tezos
XTZ: str = "XTZ"
# Thought AI
THT: str = "THT"
# TOA Coin
TOA: str = "TOA"
# Tron
TRX: str = "TRX"
# TWINS
TWINS: str = "TWINS"
# Ultimate Secure Cash
USC: str = "USC"
# Unobtanium
UNO: str = "UNO"
# Vcash
VC: str = "VC"
# Verge
XVG: str = "XVG"
# Vertcoin
VTC: str = "VTC"
# Viacoin
VIA: str = "VIA"
# Vivo
VIVO: str = "VIVO"
# Virtual Cash
VASH: str = "VASH"
# Whitecoin
XWC: str = "XWC"
# Wincoin
WC: str = "WC"
# XinFin
XDC: str = "XDC"
# XUEZ
XUEZ: str = "XUEZ"
# Ycash
YEC: str = "YEC"
# Zcash
ZEC: str = "ZEC"
# ZClassic
ZCL: str = "ZCL"
# Zencash or Horizen
ZEN: str = "ZEN"

__all__: List[str] = [
    "ALGO",
    "ANON",
    "AGM",
    "XAX",
    "AYA",
    "AC",
    "ATOM",
    "AUR",
    "AVN",
    "AXE",
    "BTA",
    "BEET",
    "BELA",
    "BTDX",
    "BTC",
    "BCH",
    "BTG",
    "XBC",
    "BSV",
    "BTCZ",
    "BTX",
    "BSD",
    "BLK",
    "BND",
    "BST",
    "BOLI",
    "BRIT",
    "CDN",
    "CCN",
    "ADA",
    "CLAM",
    "CLUB",
    "CMP",
    "CPU",
    "CRP",
    "CRAVE",
    "DASH",
    "ONION",
    "DFC",
    "DNR",
    "DMD",
    "DGB",
    "DGC",
    "DOGE",
    "ECN",
    "EDRC",
    "EMC2",
    "ELA",
    "EGLD",
    "NRG",
    "ETH",
    "ERC",
    "EVR",
    "EXCL",
    "FTC",
    "FRST",
    "FIX",
    "FLASH",
    "FLUX",
    "FOXD",
    "FJC",
    "GAME",
    "GCR",
    "GBX",
    "GRC",
    "GRS",
    "NLG",
    "HNC",
    "THC",
    "HUSH",
    "INSN",
    "IOP",
    "IXC",
    "JBS",
    "KOBO",
    "KMD",
    "LBC",
    "LINX",
    "LTC",
    "LCC",
    "LTZ",
    "LKR",
    "LYNX",
    "MZC",
    "MEC",
    "MNX",
    "MONA",
    "XMR",
    "MONK",
    "XMY",
    "NMC",
    "NAV",
    "NEBL",
    "NEO",
    "NEOS",
    "NRO",
    "NYC",
    "NIX",
    "NVC",
    "NBT",
    "NSR",
    "OK",
    "OMNI",
    "ONX",
    "PPC",
    "PSB",
    "PHR",
    "PINK",
    "PIVX",
    "POSW",
    "POT",
    "PRJ",
    "PUT",
    "QTUM",
    "RPD",
    "RVN",
    "RDD",
    "XRP",
    "RBTC",
    "RBY",
    "SAFE",
    "SLS",
    "SCRIBE",
    "SDC",
    "SLM",
    "SMLY",
    "SOL",
    "SLR",
    "STASH",
    "XLM",
    "STRAT",
    "SUGAR",
    "SYS",
    "XTZ",
    "THT",
    "TOA",
    "TRX",
    "TWINS",
    "USC",
    "UNO",
    "VC",
    "XVG",
    "VTC",
    "VIA",
    "VIVO",
    "VASH",
    "XWC",
    "WC",
    "XDC",
    "XUEZ",
    "YEC",
    "ZEC",
    "ZCL",
    "ZEN"
]
