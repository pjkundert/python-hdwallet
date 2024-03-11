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
from .auroracoin import Auroracoin
from .avian import Avian
from .axe import Axe
from .bata import Bata
from .beetlecoin import BeetleCoin
from .belacoin import BelaCoin
from .bitcloud import BitCloud
from .bitcoin import Bitcoin
from .bitcoinatom import BitcoinAtom
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
from .compcoin import Compcoin
from .cosmos import Cosmos
from .cpuchain import CPUChain
from .cranepay import CranePay
from .crave import Crave
from .dash import Dash
from .deeponion import DeepOnion
from .defcoin import Defcoin
from .denarius import Denarius
from .diamond import Diamond
from .digibyte import DigiByte
from .digitalcoin import Digitalcoin
from .dogecoin import Dogecoin
from .ecoin import ECoin
from .edrcoin import EDRCoin
from .einsteinium import Einsteinium
from .elastos import Elastos
from .elrond import Elrond
from .energi import Energi
from .ethereum import Ethereum
from .europecoin import EuropeCoin
from .evrmore import Evrmore
from .exclusivecoin import ExclusiveCoin
from .feathercoin import Feathercoin
from .firstcoin import Firstcoin
from .fix import FIX
from .flashcoin import Flashcoin
from .flux import Flux
from .foxdcoin import Foxdcoin
from .fujicoin import FujiCoin
from .gamecredits import GameCredits
from .gcrcoin import GCRCoin
from .gobyte import GoByte
from .gridcoin import Gridcoin
from .groestlcoin import GroestlCoin
from .gulden import Gulden
from .helleniccoin import Helleniccoin
from .hempcoin import Hempcoin
from .horizen import Horizen
from .hush import Hush
from .insanecoin import InsaneCoin
from .internetofpeople import InternetOfPeople
from .ixcoin import IXCoin
from .jumbucks import Jumbucks
from .kobocoin import Kobocoin
from .komodo import Komodo
from .lbrycredits import LBRYCredits
from .linx import Linx
from .litecoin import Litecoin
from .litecoincash import LitecoinCash
from .litecoinz import LitecoinZ
from .lkrcoin import Lkrcoin
from .lynx import Lynx
from .mazacoin import Mazacoin
from .megacoin import Megacoin
from .minexcoin import Minexcoin
from .monacoin import Monacoin
from .monero import Monero
from .monk import Monk
from .monkeyproject import MonkeyProject
from .multiversx import MultiversX
from .myriadcion import Myriadcoin
from .namecoin import Namecoin
from .navcoin import Navcoin
from .neblio import Neblio
from .neo import Neo
from .neoscoin import Neoscoin
from .neurocoin import Neurocoin
from .newyorkcoin import NewYorkCoin
from .nix import NIX
from .novacoin import Novacoin
from .nubits import NuBits
from .nushares import NuShares
from .okcash import OKCash
from .omni import Omni
from .onix import Onix
from .peercoin import Peercoin
from .pesobit import Pesobit
from .phore import Phore
from .pinkcoin import Pinkcoin
from .pivx import Pivx
from .poswcoin import PoSWCoin
from .potcoin import Potcoin
from .projectcoin import ProjectCoin
from .putincoin import Putincoin
from .qtum import Qtum
from .rapids import Rapids
from .ravencoin import Ravencoin
from .reddcoin import Reddcoin
from .ripple import Ripple
from .rsk import RSK
from .rubycoin import Rubycoin
from .safecoin import Safecoin
from .saluscoin import Saluscoin
from .scribe import Scribe
from .shadowcash import ShadowCash
from .slimcoin import Slimcoin
from .smileycoin import Smileycoin
from .solana import Solana
from .solarcoin import Solarcoin
from .stash import Stash
from .stellar import Stellar
from .stratis import Stratis
from .sugarchain import Sugarchain
from .syscoin import Syscoin
from .tezos import Tezos
from .thoughtai import ThoughtAI
from .toacoin import TOACoin
from .tron import Tron
from .twins import TWINS
from .ultimatesecurecash import UltimateSecureCash
from .unobtanium import Unobtanium
from .vcash import Vcash
from .verge import Verge
from .vertcoin import Vertcoin
from .viacoin import Viacoin
from .vivo import Vivo
from .vpncoin import VPNCoin
from .whitecoin import Whitecoin
from .wincoin import Wincoin
from .xinfin import XinFin
from .xuez import XUEZ
from .ycash import Ycash
from .zcash import Zcash
from .zclassic import ZClassic
from .zencash import Zencash

CRYPTOCURRENCIES: Dict[str, Type[ICryptocurrency]] = {
    Algorand.NAME: Algorand,
    Anon.NAME: Anon,
    Argoneum.NAME: Argoneum,
    Artax.NAME: Artax,
    Aryacoin.NAME: Aryacoin,
    Asiacoin.NAME: Asiacoin,
    Auroracoin.NAME: Auroracoin,
    Avian.NAME: Avian,
    Axe.NAME: Axe,
    Bata.NAME: Bata,
    BeetleCoin.NAME: BeetleCoin,
    BelaCoin.NAME: BelaCoin,
    BitCloud.NAME: BitCloud,
    Bitcoin.NAME: Bitcoin,
    BitcoinAtom.NAME: BitcoinAtom,
    BitcoinCash.NAME: BitcoinCash,
    BitcoinGold.NAME: BitcoinGold,
    BitcoinPlus.NAME: BitcoinPlus,
    BitcoinSV.NAME: BitcoinSV,
    BitcoinZ.NAME: BitcoinZ,
    Bitcore.NAME: Bitcore,
    BitSend.NAME: BitSend,
    Blackcoin.NAME: Blackcoin,
    Blocknode.NAME: Blocknode,
    BlockStamp.NAME: BlockStamp,
    Bolivarcoin.NAME: Bolivarcoin,
    BritCoin.NAME: BritCoin,
    CanadaECoin.NAME: CanadaECoin,
    Cannacoin.NAME: Cannacoin,
    Cardano.NAME: Cardano,
    Clams.NAME: Clams,
    ClubCoin.NAME: ClubCoin,
    Compcoin.NAME: Compcoin,
    Cosmos.NAME: Cosmos,
    CPUChain.NAME: CPUChain,
    CranePay.NAME: CranePay,
    Crave.NAME: Crave,
    Dash.NAME: Dash,
    DeepOnion.NAME: DeepOnion,
    Defcoin.NAME: Defcoin,
    Denarius.NAME: Denarius,
    Diamond.NAME: Diamond,
    DigiByte.NAME: DigiByte,
    Digitalcoin.NAME: Digitalcoin,
    Dogecoin.NAME: Dogecoin,
    ECoin.NAME: ECoin,
    EDRCoin.NAME: EDRCoin,
    Einsteinium.NAME: Einsteinium,
    Elastos.NAME: Elastos,
    Elrond.NAME: Elrond,
    Energi.NAME: Energi,
    Ethereum.NAME: Ethereum,
    EuropeCoin.NAME: EuropeCoin,
    Evrmore.NAME: Evrmore,
    ExclusiveCoin.NAME: ExclusiveCoin,
    Feathercoin.NAME: Feathercoin,
    Firstcoin.NAME: Firstcoin,
    FIX.NAME: FIX,
    Flashcoin.NAME: Flashcoin,
    Flux.NAME: Flux,
    Foxdcoin.NAME: Foxdcoin,
    FujiCoin.NAME: FujiCoin,
    GameCredits.NAME: GameCredits,
    GCRCoin.NAME: GCRCoin,
    GoByte.NAME: GoByte,
    Gridcoin.NAME: Gridcoin,
    GroestlCoin.NAME: GroestlCoin,
    Gulden.NAME: Gulden,
    Helleniccoin.NAME: Helleniccoin,
    Hempcoin.NAME: Hempcoin,
    Horizen.NAME: Horizen,
    Hush.NAME: Hush,
    InsaneCoin.NAME: InsaneCoin,
    InternetOfPeople.NAME: InternetOfPeople,
    IXCoin.NAME: IXCoin,
    Jumbucks.NAME: Jumbucks,
    Kobocoin.NAME: Kobocoin,
    Komodo.NAME: Komodo,
    LBRYCredits.NAME: LBRYCredits,
    Linx.NAME: Linx,
    Litecoin.NAME: Litecoin,
    LitecoinCash.NAME: LitecoinCash,
    LitecoinZ.NAME: LitecoinZ,
    Lkrcoin.NAME: Lkrcoin,
    Lynx.NAME: Lynx,
    Mazacoin.NAME: Mazacoin,
    Megacoin.NAME: Megacoin,
    Minexcoin.NAME: Minexcoin,
    Monacoin.NAME: Monacoin,
    Monero.NAME: Monero,
    Monk.NAME: Monk,
    MonkeyProject.NAME: MonkeyProject,
    MultiversX.NAME: MultiversX,
    Myriadcoin.NAME: Myriadcoin,
    Namecoin.NAME: Namecoin,
    Navcoin.NAME: Navcoin,
    Neblio.NAME: Neblio,
    Neo.NAME: Neo,
    Neoscoin.NAME: Neoscoin,
    Neurocoin.NAME: Neurocoin,
    NewYorkCoin.NAME: NewYorkCoin,
    NIX.NAME: NIX,
    Novacoin.NAME: Novacoin,
    NuBits.NAME: NuBits,
    NuShares.NAME: NuShares,
    OKCash.NAME: OKCash,
    Omni.NAME: Omni,
    Onix.NAME: Onix,
    Peercoin.NAME: Peercoin,
    Pesobit.NAME: Pesobit,
    Phore.NAME: Phore,
    Pinkcoin.NAME: Pinkcoin,
    Pivx.NAME: Pivx,
    PoSWCoin.NAME: PoSWCoin,
    Potcoin.NAME: Potcoin,
    ProjectCoin.NAME: ProjectCoin,
    Putincoin.NAME: Putincoin,
    Qtum.NAME: Qtum,
    Rapids.NAME: Rapids,
    Ravencoin.NAME: Ravencoin,
    Reddcoin.NAME: Reddcoin,
    Ripple.NAME: Ripple,
    RSK.NAME: RSK,
    Rubycoin.NAME: Rubycoin,
    Safecoin.NAME: Safecoin,
    Saluscoin.NAME: Saluscoin,
    Scribe.NAME: Scribe,
    ShadowCash.NAME: ShadowCash,
    Slimcoin.NAME: Slimcoin,
    Smileycoin.NAME: Smileycoin,
    Solana.NAME: Solana,
    Solarcoin.NAME: Solarcoin,
    Stash.NAME: Stash,
    Stellar.NAME: Stellar,
    Stratis.NAME: Stratis,
    Sugarchain.NAME: Sugarchain,
    Syscoin.NAME: Syscoin,
    Tezos.NAME: Tezos,
    ThoughtAI.NAME: ThoughtAI,
    TOACoin.NAME: TOACoin,
    Tron.NAME: Tron,
    TWINS.NAME: TWINS,
    UltimateSecureCash.NAME: UltimateSecureCash,
    Unobtanium.NAME: Unobtanium,
    Vcash.NAME: Vcash,
    Verge.NAME: Verge,
    Vertcoin.NAME: Vertcoin,
    Viacoin.NAME: Viacoin,
    Vivo.NAME: Vivo,
    VPNCoin.NAME: VPNCoin,
    Whitecoin.NAME: Whitecoin,
    Wincoin.NAME: Wincoin,
    XinFin.NAME: XinFin,
    XUEZ.NAME: XUEZ,
    Ycash.NAME: Ycash,
    Zcash.NAME: Zcash,
    ZClassic.NAME: ZClassic,
    Zencash.NAME: Zencash
}

__all__: List[str] = ["ICryptocurrency", "CRYPTOCURRENCIES"] + [
    cryptocurrency.__name__ for cryptocurrency in CRYPTOCURRENCIES.values()
]
