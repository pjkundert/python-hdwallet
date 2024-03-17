#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    List, Dict, Type
)

from .iaddress import IAddress
from .algorand import AlgorandAddress
from .aptos import AptosAddress
from .avalanche import AvalancheAddress
from .cardano import CardanoAddress
from .cosmos import CosmosAddress
from .eos import EOSAddress
from .ergo import ErgoAddress
from .ethereum import EthereumAddress
from .filecoin import FilecoinAddress
from .harmony import HarmonyAddress
from .icon import IconAddress
from .injective import InjectiveAddress
from .monero import MoneroAddress
from .multiversx import MultiversXAddress
from .nano import NanoAddress
from .near import NearAddress
from .neo import NeoAddress
from .okt_chain import OKTChainAddress
from .p2pkh import P2PKHAddress
from .p2sh import P2SHAddress
from .p2tr import P2TRAddress
from .p2wpkh import P2WPKHAddress
from .p2wpkh_in_p2sh import P2WPKHInP2SHAddress
from .p2wsh import P2WSHAddress
from .p2wsh_in_p2sh import P2WSHInP2SHAddress
from .ripple import RippleAddress
from .solana import SolanaAddress
from .stellar import StellarAddress
from .sui import SuiAddress
from .tezos import TezosAddress
from .tron import TronAddress
from .xinfin import XinFinAddress
from .zilliqa import ZilliqaAddress

ADDRESSES: Dict[str, Type[IAddress]] = {
    AlgorandAddress.name(): AlgorandAddress,
    AptosAddress.name(): AptosAddress,
    AvalancheAddress.name(): AvalancheAddress,
    CardanoAddress.name(): CardanoAddress,
    CosmosAddress.name(): CosmosAddress,
    EOSAddress.name(): EOSAddress,
    ErgoAddress.name(): ErgoAddress,
    EthereumAddress.name(): EthereumAddress,
    FilecoinAddress.name(): FilecoinAddress,
    HarmonyAddress.name(): HarmonyAddress,
    IconAddress.name(): IconAddress,
    InjectiveAddress.name(): InjectiveAddress,
    MoneroAddress.name(): MoneroAddress,
    MultiversXAddress.name(): MultiversXAddress,
    NanoAddress.name(): NanoAddress,
    NearAddress.name(): NearAddress,
    NeoAddress.name(): NeoAddress,
    OKTChainAddress.name(): OKTChainAddress,
    P2PKHAddress.name(): P2PKHAddress,
    P2SHAddress.name(): P2SHAddress,
    P2TRAddress.name(): P2TRAddress,
    P2WPKHAddress.name(): P2WPKHAddress,
    P2WPKHInP2SHAddress.name(): P2WPKHInP2SHAddress,
    P2WSHAddress.name(): P2WSHAddress,
    P2WSHInP2SHAddress.name(): P2WSHInP2SHAddress,
    RippleAddress.name(): RippleAddress,
    SolanaAddress.name(): SolanaAddress,
    StellarAddress.name(): StellarAddress,
    SuiAddress.name(): SuiAddress,
    TezosAddress.name(): TezosAddress,
    TronAddress.name(): TronAddress,
    XinFinAddress.name(): XinFinAddress,
    ZilliqaAddress.name(): ZilliqaAddress
}

__all__: List[str] = ["IAddress", "ADDRESSES"] + [
    address.__name__ for address in ADDRESSES.values()
]
