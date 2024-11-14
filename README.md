# Hierarchical Deterministic (HD) Wallet v3.0.0-Alpha-11

[![Build Status](https://app.travis-ci.com/meherett/python-hdwallet.svg?branch=master)](https://app.travis-ci.com/meherett/python-hdwallet)
[![PyPI Version](https://img.shields.io/pypi/v/hdwallet.svg?color=blue)](https://pypi.org/project/hdwallet)
[![Documentation Status](https://readthedocs.org/projects/hdwallet/badge/?version=master)](https://hdwallet.readthedocs.io)
[![PyPI License](https://img.shields.io/pypi/l/hdwallet?color=black)](https://pypi.org/project/hdwallet)
[![PyPI Python Version](https://img.shields.io/pypi/pyversions/hdwallet.svg)](https://pypi.org/project/hdwallet)
[![Coverage Status](https://coveralls.io/repos/github/meherett/python-hdwallet/badge.svg?branch=master)](https://coveralls.io/github/meherett/python-hdwallet)

Python-based library for the implementation of a hierarchical deterministic wallet generator for more than 140+ multiple cryptocurrencies.
It allows the handling of multiple coins, multiple accounts, external and internal chains per account and millions of addresses per chain.

![HDWallet-CLI](https://raw.githubusercontent.com/meherett/python-hdwallet/master/docs/static/svg/hdwallet-cli.svg)

For more info see the BIP specs.

| BIP's                                                                    | Titles                                                     |
| :----------------------------------------------------------------------- | :--------------------------------------------------------- |
| [BIP39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)  | Mnemonic code for generating deterministic keys            |
| [BIP85](https://github.com/bitcoin/bips/blob/master/bip-0085.mediawiki)  | Deterministic Entropy From BIP32 Keychains                 |
| [BIP32](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki)  | Hierarchical Deterministic Wallets                         |
| [BIP44](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki)  | Multi-Account Hierarchy for Deterministic Wallets          |
| [BIP49](https://github.com/bitcoin/bips/blob/master/bip-0049.mediawiki)  | Derivation scheme for P2WPKH-nested-in-P2SH based accounts |
| [BIP84](https://github.com/bitcoin/bips/blob/master/bip-0084.mediawiki)  | Derivation scheme for P2WPKH based accounts                |
| [BIP141](https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki) | Segregated Witness (Consensus layer)                       |

## Installation

The easiest way to install `hdwallet` is via pip:

```
pip install hdwallet
```

To install `hdwallet` command line interface globally, for Linux `sudo` may be required:

```
pip install hdwallet[cli]
```

If you want to run the latest version of the code, you can install from the git:

```
pip install git+git://github.com/meherett/python-hdwallet.git
```

For the versions available, see the [tags on this repository](https://github.com/meherett/python-hdwallet/tags).

## Quick Usage

Simple Bitcoin mainnet HDWallet generator:

```python
#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.utils import generate_entropy
from hdwallet.symbols import BTC as SYMBOL
from typing import Optional

import json

# Choose strength 128, 160, 192, 224 or 256
STRENGTH: int = 160  # Default is 128
# Choose language english, french, italian, spanish, chinese_simplified, chinese_traditional, japanese or korean
LANGUAGE: str = "korean"  # Default is english
# Generate new entropy hex string
ENTROPY: str = generate_entropy(strength=STRENGTH)
# Secret passphrase for mnemonic
PASSPHRASE: Optional[str] = None  # "meherett"

# Initialize Bitcoin mainnet HDWallet
hdwallet: HDWallet = HDWallet(symbol=SYMBOL, use_default_path=False)
# Get Bitcoin HDWallet from entropy
hdwallet.from_entropy(
    entropy=ENTROPY, language=LANGUAGE, passphrase=PASSPHRASE
)

# Derivation from path
# hdwallet.from_path("m/44'/0'/0'/0/0")
# Or derivation from index
hdwallet.from_index(44, hardened=True)
hdwallet.from_index(0, hardened=True)
hdwallet.from_index(0, hardened=True)
hdwallet.from_index(0)
hdwallet.from_index(0)

# Print all Bitcoin HDWallet information's
print(json.dumps(hdwallet.dumps(), indent=4, ensure_ascii=False))
```

<details open>
  <summary>Output</summary><br/>

```json5
{
    "cryptocurrency": "Bitcoin",
    "symbol": "BTC",
    "network": "mainnet",
    "strength": 160,
    "entropy": "c5b0d0ee698f3f72b6265f1bc591f8f2d7afa6dd",
    "mnemonic": "주일 액수 명단 천둥 해수욕장 전망 추천 직업 그룹 단위 신체 파란색 시청 천천히 스트레스",
    "language": "korean",
    "passphrase": null,
    "seed": "5a9b9667ccd07b3c641b1ba95e9119dd1d5a3034fd46cd2f27fc1f160c7dcd824fc0ab4710a9ae90582dffc3b0803bcbc0a8160feeaab4c70511c5035859decf",
    "root_xprivate_key": "xprv9s21ZrQH143K2qMHU8aghJ4MoQR5g5mowXbeP2vCP937bseZGX929dmJudL7u4xRxtKvh58pxz1PhtCbWW2yUH14jdduKVMV9FkBMpM2Hyw",
    "root_xpublic_key": "xpub661MyMwAqRbcFKRkaA7h4S16MSFa5YVfJkXFBRKowUa6Ufyhp4TGhS5nkvkLXSmdNjoszzDkU26WW2rg1zBsQBt6Pv3T8oLEAExGHD3hcQs",
    "xprivate_key": "xprvA2YyMZWyPK2xo4eZgyypp2CzcHnxNzGbruGg7vmgaAVCtBtrjwzuhXJBNM3FrwBh85ajxHErNR6ByN77WJARpC1HDC7kTwa2yr7Mu9Pz5Qq",
    "xpublic_key": "xpub6FYKm53sDgbG1Yj2o1WqBA9jAKdSnSzTE8CGvKBJ8W2BkzE1HVKAFKcfDcCHKpL5BQRg2HjbNSt55jpFshY7W1KFtp7zjB3DhNAmiFv6kzB",
    "uncompressed": "081016370b45d7e23bd89b07d6886036f5e4df9a129eee3b488c177ba7881856e24d337b280f9d32539a22445e567543b39b708edf5289442f36dcde958a3433",
    "compressed": "03081016370b45d7e23bd89b07d6886036f5e4df9a129eee3b488c177ba7881856",
    "chain_code": "cf9ee427ed8073e009a5743056e8cf19167f67ca5082c2c6635b391e9a4e0b0d",
    "private_key": "f79495fda777197ce73551bcd8e162ceca19167575760d3cc2bced4bf2a213dc",
    "public_key": "03081016370b45d7e23bd89b07d6886036f5e4df9a129eee3b488c177ba7881856",
    "wif": "L5WyVfBu8Sz3iGZtrwJVSP2wDJmu7HThGd1EGekFBnviWgzLXpJd",
    "finger_print": "ac13e305",
    "semantic": "p2pkh",
    "path": "m/44'/0'/0'/0/0",
    "hash": "ac13e305a88bd9968f1c058fcf5d9a6b1b9ef484",
    "addresses": {
        "p2pkh": "1Ggs3kkNrPPWoW17iDFQWgMdw3CD8BzBiv",
        "p2sh": "3GQVUFePz517Hf61Vsa9H2tHj5jw5y6ngV",
        "p2wpkh": "bc1q4sf7xpdg30vedrcuqk8u7hv6dvdeaayy3uw5cj",
        "p2wpkh_in_p2sh": "3JyV5aSgdVYEjQodPWHfvehQ5227EDr3sN",
        "p2wsh": "bc1qnk0s9q4379n6v9vg0lnhdu5qhjyx99u2xm238pmckmjg9v29q54saddzp9",
        "p2wsh_in_p2sh": "3MmsEoP7GLHzuLVgkAtcRtyXLTWh8zNAcd"
    }
}
```
</details>

Ethereum mainnet [Ganache](https://github.com/trufflesuite/ganache) wallet look's like:

```python
#!/usr/bin/env python3

from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic
from typing import Optional

# Generate english mnemonic words
MNEMONIC: str = generate_mnemonic(language="english", strength=128)
# Secret passphrase/password for mnemonic
PASSPHRASE: Optional[str] = None  # "meherett"

# Initialize Ethereum mainnet BIP44HDWallet
bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
# Get Ethereum BIP44HDWallet from mnemonic
bip44_hdwallet.from_mnemonic(
    mnemonic=MNEMONIC, language="english", passphrase=PASSPHRASE
)
# Clean default BIP44 derivation indexes/paths
bip44_hdwallet.clean_derivation()

print("Mnemonic:", bip44_hdwallet.mnemonic())
print("Base HD Path:  m/44'/60'/0'/0/{address_index}", "\n")

# Get Ethereum BIP44HDWallet information's from address index
for address_index in range(10):
    # Derivation from Ethereum BIP44 derivation path
    bip44_derivation: BIP44Derivation = BIP44Derivation(
        cryptocurrency=EthereumMainnet, account=0, change=False, address=address_index
    )
    # Drive Ethereum BIP44HDWallet
    bip44_hdwallet.from_path(path=bip44_derivation)
    # Print address_index, path, address and private_key
    print(f"({address_index}) {bip44_hdwallet.path()} {bip44_hdwallet.address()} 0x{bip44_hdwallet.private_key()}")
    # Clean derivation indexes/paths
    bip44_hdwallet.clean_derivation()
```

<details open>
  <summary>Output</summary><br/>

```shell script
Mnemonic: bright demand olive glance crater key head glory quantum leisure intact age
Base HD Path:  m/44'/60'/0'/0/{address_index}

(0) m/44'/60'/0'/0/0 0x3a149f0c5dc5c0F1E29e573215C23710dE9c4f87 0xa45f9af43912fdd5e88c492226be082029f257681d4b3e73b68be535d2fb0526
(1) m/44'/60'/0'/0/1 0x9e8A4fD9bA74DbB0c7F465EF56b47489793AA102 0x6e5ab2a3ae20c7b3a1c0645b03689e88e8cdff16f6a39d6a420bfebc20e8a941
(2) m/44'/60'/0'/0/2 0x08Eb0646ddc52E12a03215b94b244B674e9D7a0F 0x938caf07197eda13679bfd88df7e5f6eac3cd9f9248ed445f1a0e084a3e9417c
(3) m/44'/60'/0'/0/3 0x6dB1Ac10bbbE7bdc6bcB246E2Dd36884c346CbE8 0x304e9bebaeef3f4ae7c4d2ef268f40f503d8f47fd2621a575d8f73f49762cbc0
(4) m/44'/60'/0'/0/4 0xd528281f804D950c743Ca48FCcC3D76A3d9AcD5C 0x82a0284b443ec73884806ac9450f09110d8dba024120985431b80a520b3f2911
(5) m/44'/60'/0'/0/5 0xaF24cc02Fd5E0285237677cDDD00ae8E4a9d6E5E 0xb03c61e992f5475222295077a89cf35011984dcdcd1da3666ebffc9ebefe22a9
(6) m/44'/60'/0'/0/6 0x55A972f207DB3498DCBbD97062472A5c10b3266b 0xc003175828a6f768610fb2396b3fcec7fa1957770de2462b9e6d3a0a23346c76
(7) m/44'/60'/0'/0/7 0x7e62C187e597Fc544D5769a38A8e026F5529c81B 0x04bfcff46587fd98e682e3b7acff720051b1b0bee3309fb13703338bbde211cd
(8) m/44'/60'/0'/0/8 0x7aF4A78000032a3FBaF4Ac5a5f64a50FF69f0442 0x1b642b77519cf6e6107827e4773a15975edda6471ff90735e2fc0cf7d8560ac8
(9) m/44'/60'/0'/0/9 0x379a25BB89043f8b875A73eA61aF4F7b70cD73e5 0x4f9fb333faf8ecf8f22d212a0b1c946e4d4c32fa0b7794326038d464b241d771
```
</details>

[Click this to see more examples :)](https://github.com/meherett/python-hdwallet/blob/master/examples)

## Development

To get started, just fork this repo, clone it locally, and run:

```
pip install -e .[cli,tests,docs] -r requirements.txt
```

## Testing

You can run the tests with:

```
pytest
```

Or use `tox` to run the complete suite against the full set of build targets, or pytest to run specific 
tests against a specific version of Python.

## Contributing

Feel free to open an [issue](https://github.com/meherett/hdwallet/issues) if you find a problem,
or a pull request if you've solved an issue. And also any help in testing, development,
documentation and other tasks is highly appreciated and useful to the project.
There are tasks for contributors of all experience levels.

For more information, see the [CONTRIBUTING.md](https://github.com/meherett/hdwallet/blob/master/CONTRIBUTING.md) file.

## Available Cryptocurrencies

This library simplifies the process of creating a new hierarchical deterministic wallets for:

Name                                                                       | Symbol | Coin Type | Networks                         | ECC                    | HDs                                                                                 | BIP38              | Addresses                                                                     |
:--------------------------------------------------------------------------|:------:|:---------:|:--------------------------------:|:----------------------:|:-----------------------------------------------------------------------------------:|:------------------:|:-----------------------------------------------------------------------------:|
[Adcoin](https://github.com/adcoin-project/AdCoin)                         | ACC    | 161       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Akash-Network](https://github.com/akash-network)                          | AKT    | 118       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Cosmos`                                                                      |
[Algorand](https://github.com/algorand/go-algorand)                        | ALGO   | 283       | `mainnet`                        | SLIP10-Ed25519         | `BIP44`, `BIP32`                                                                    | :x:                | `Algorand`                                                                    |
[Anon](https://github.com/anonymousbitcoin/anon)                           | ANON   | 220       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Aptos](https://github.com/aptos-labs)                                     | APT    | 637       | `mainnet`                        | SLIP10-Ed25519         | `BIP44`, `BIP32`                                                                    | :x:                | `Aptos`                                                                       |
[Arbitrum](https://arbitrum.foundation)                                    | ARB    | 60        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Ethereum`                                                                    |
[Argoneum](https://github.com/Argoneum/argoneum)                           | AGM    | 421       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Artax](https://github.com/artax-committee/Artax)                          | XAX    | 219       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Aryacoin](https://github.com/Aryacoin/Aryacoin)                           | AYA    | 357       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Asiacoin](http://www.thecoin.asia)                                        | AC     | 51        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Auroracoin](https://github.com/aurarad/auroracoin)                        | AUR    | 85        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Avalanche](https://github.com/ava-labs/avalanchego)                       | AVAX   | 9000      | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Avalanche`, `Ethereum`                                                       |
[Avian](https://github.com/AvianNetwork/Avian)                             | AVN    | 921       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`, `P2WSH`, `P2WSH-In-P2SH`         |
[Axe](https://github.com/AXErunners/axe)                                   | AXE    | 4242      | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Axelar](https://github.com/axelarnetwork/axelar-core)                     | AXL    | 118       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Cosmos`                                                                      |
[Band-Protocol](https://github.com/bandprotocol/chain)                     | BAND   | 494       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Cosmos`                                                                      |
[Bata](https://github.com/BTA-BATA/Bataoshi)                               | BTA    | 89        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Beetle-Coin](https://github.com/beetledev/Wallet)                         | BEET   | 800       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Bela-Coin](https://github.com/TheAmbiaFund/erc20bela)                     | BELA   | 73        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Binance](https://github.com/bnb-chain/bsc)                                | BNB    | 714       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Cosmos`, `Ethereum`                                                          |
[Bit-Cloud](https://github.com/LIMXTEC/Bitcloud)                           | BTDX   | 218       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Bitcoin](https://github.com/bitcoin/bitcoin)                              | BTC    | 0         | `mainnet`, `testnet`, `regtest`  | SLIP10-Secp256k1       | `BIP32`, `BIP44`, `BIP49`, `BIP84`, `BIP86`, `BIP141`, `Electrum-V1`, `Electrum-V2` | :white_check_mark: | `P2PKH`, `P2SH`, `P2TR`, `P2WPKH`, `P2WPKH-In-P2SH`, `P2WSH`, `P2WSH-In-P2SH` |
[Bitcoin-Atom](https://github.com/bitcoin-atom/bitcoin-atom)               | BCA    | 185       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`                                   |
[Bitcoin-Cash](https://github.com/bitcoincashorg/bitcoincash.org)          | BCH    | 145       | `mainnet`, `testnet`, `regtest`  | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`, `P2WSH`, `P2WSH-In-P2SH`         |
[Bitcoin-Cash-SLP](https://github.com/bitcoincashorg/bitcoincash.org)      | SLP    | 145       | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`, `P2WSH`, `P2WSH-In-P2SH`         |
[Bitcoin-Gold](https://github.com/BTCGPU/BTCGPU)                           | BTG    | 156       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`, `P2WSH`, `P2WSH-In-P2SH`         |
[Bitcoin-Green](https://github.com/bitcoin-green/bitcoingreen)             | BITG   | 222       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Bitcoin-Plus](https://github.com/bitcoinplusorg/xbcwalletsource)          | XBC    | 65        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Bitcoin-Private](https://github.com/BTCPrivate/BitcoinPrivate)            | BTCP   | 183       | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Bitcoin-SV](https://github.com/bitcoin-sv/bitcoin-sv)                     | BSV    | 236       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[BitcoinZ](https://github.com/btcz/bitcoinz)                               | BTCZ   | 177       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Bitcore](https://github.com/bitcore-btx/BitCore)                          | BTX    | 160       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`                                   |
[Bit-Send](https://github.com/LIMXTEC/BitSend)                             | BSD    | 91        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Blackcoin](https://github.com/coinblack)                                  | BLK    | 10        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Blocknode](https://github.com/blocknodetech/blocknode)                    | BND    | 2941      | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Block-Stamp](https://github.com/BlockStamp)                               | BST    | 254       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`                                   |
[Bolivarcoin](https://github.com/BOLI-Project/BolivarCoin)                 | BOLI   | 278       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Brit-Coin](https://github.com/britcoin3)                                  | BRIT   | 70        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Canada-eCoin](https://github.com/Canada-eCoin)                            | CDN    | 34        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Cannacoin](https://github.com/cannacoin-official/Cannacoin)               | CCN    | 19        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Cardano](https://cardanoupdates.com)                                      | ADA    | 1815      | `mainnet`, `testnet`             | Kholaw-Ed25519         | `Cardano`                                                                           | :x:                | `Cardano`                                                                     |
[Celo](https://github.com/celo-org/celo-monorepo)                          | CELO   | 52752     | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Ethereum`                                                                    |
[Chihuahua](http://chihuahua.army)                                         | HUA    | 118       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Cosmos`                                                                      |
[Clams](https://github.com/nochowderforyou/clams)                          | CLAM   | 23        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Club-Coin](https://github.com/BitClubDev/ClubCoin)                        | CLUB   | 79        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Compcoin](https://compcoin.com)                                           | CMP    | 71        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Cosmos](https://github.com/cosmos)                                        | ATOM   | 118       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Cosmos`                                                                      |
[CPU-Chain](https://github.com/cpuchain/cpuchain)                          | CPU    | 363       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`                                   |
[Crane-Pay](https://github.com/cranepay/cranepay-core)                     | CRP    | 2304      | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`                                   |
[Crave](https://github.com/Crave-Community-Project/Crave-Project)          | CRAVE  | 186       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Dash](https://github.com/dashpay/dash)                                    | DASH   | 5         | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[DeepOnion](https://github.com/deeponion/deeponion)                        | ONION  | 305       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`                                   |
[Defcoin](https://github.com/mspicer/Defcoin)                              | DFC    | 1337      | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Denarius](https://github.com/metaspartan/denarius)                        | DNR    | 116       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Diamond](https://github.com/DMDcoin/Diamond)                              | DMD    | 152       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Digi-Byte](https://github.com/DigiByte-Core/digibyte)                     | DGB    | 20        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`                                   |
[Digitalcoin](https://github.com/lomtax/digitalcoin)                       | DGC    | 18        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Divi](https://github.com/Divicoin/Divi)                                   | DIVI   | 301       | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Dogecoin](https://github.com/dogecoin/dogecoin)                           | DOGE   | 3         | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`                                   |
[eCash](https://github.com/bitcoin-abc)                                    | XEC    | 145       | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`, `P2WSH`, `P2WSH-In-P2SH`         |
[E-coin](https://github.com/ecoinclub/ecoin)                               | ECN    | 115       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[EDR-Coin](https://github.com/EDRCoin/EDRcoin-src)                         | EDRC   | 56        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[e-Gulden](https://github.com/Electronic-Gulden-Foundation/egulden)        | EFL    | 78        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Einsteinium](https://github.com/emc2foundation/einsteinium)               | EMC2   | 41        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Elastos](https://github.com/elastos)                                      | ELA    | 2305      | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Energi](https://github.com/energicryptocurrency/go-energi)                | NRG    | 9797      | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[EOS](https://github.com/AntelopeIO/leap)                                  | EOS    | 194       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `EOS`                                                                         |
[Ergo](https://github.com/ergoplatform/ergo)                               | ERG    | 429       | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Ergo`                                                                        |
[Ethereum](https://github.com/ethereum/go-ethereum)                        | ETH    | 60        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Ethereum`                                                                    |
[Europe-Coin](https://github.com/LIMXTEC/Europecoin-V3)                    | ERC    | 151       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Evrmore](https://github.com/EvrmoreOrg/Evrmore)                           | EVR    | 175       | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`, `P2WSH`, `P2WSH-In-P2SH`         |
[Exclusive-Coin](https://github.com/exclfork/excl-core)                    | EXCL   | 190       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Fantom](https://github.com/Fantom-foundation/go-opera)                    | FTM    | 60        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Ethereum`                                                                    |
[Feathercoin](https://github.com/FeatherCoin/Feathercoin)                  | FTC    | 8         | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Fetch.ai](https://github.com/fetchai)                                     | FET    | 118       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Cosmos`                                                                      |
[Filecoin](https://github.com/filecoin-project)                            | FIL    | 461       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Filecoin`                                                                    |
[Firo](https://github.com/firoorg/firo)                                    | FIRO   | 136       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Firstcoin](http://firstcoinproject.com)                                   | FRST   | 167       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[FIX](https://github.com/NewCapital/FIX-Core)                              | FIX    | 336       | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Flashcoin](https://github.com/flash-coin)                                 | FLASH  | 120       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Flux](https://github.com/RunOnFlux/fluxd)                                 | FLUX   | 19167     | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Foxdcoin](https://github.com/foxdproject/foxdcoin)                        | FOXD   | 175       | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`, `P2WSH`, `P2WSH-In-P2SH`         |
[Fuji-Coin](https://github.com/fujicoin/fujicoin)                          | FJC    | 75        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`                                   |
[Game-Credits](https://github.com/gamecredits-project/GameCredits)         | GAME   | 101       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[GCR-Coin](https://globalcoinresearch.com)                                 | GCR    | 49        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Go-Byte](https://github.com/gobytecoin/gobyte)                            | GBX    | 176       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Gridcoin](https://github.com/gridcoin-community/Gridcoin-Research)        | GRC    | 84        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Groestl-Coin](https://github.com/Groestlcoin/groestlcoin)                 | GRS    | 17        | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`                                   |
[Gulden](https://github.com/Gulden/gulden-old)                             | NLG    | 87        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Harmony](https://github.com/harmony-one/harmony)                          | ONE    | 1023      | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Harmony`                                                                     |
[Helleniccoin](https://github.com/hnc-coin/hnc-coin)                       | HNC    | 168       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Hempcoin](https://github.com/jl777/komodo)                                | THC    | 113       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Horizen](https://github.com/HorizenOfficial/zen)                          | ZEN    | 121       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Huobi-Token](https://www.huobi.com/en-us)                                 | HT     | 553       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Ethereum`                                                                    |
[Hush](https://git.hush.is/hush/hush3)                                     | HUSH   | 197       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Icon](https://github.com/icon-project)                                    | ICX    | 74        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Icon`                                                                        |
[Injective](https://github.com/InjectiveLabs)                              | INJ    | 60        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Injective`                                                                   |
[InsaneCoin](https://github.com/CryptoCoderz/INSN)                         | INSN   | 68        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Internet-Of-People](https://github.com/Internet-of-People)                | IOP    | 66        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[IRISnet](https://github.com/irisnet)                                      | IRIS   | 566       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Cosmos`                                                                      |
[IX-Coin](https://github.com/ixcore/ixcoin)                                | IXC    | 86        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Jumbucks](http://getjumbucks.com)                                         | JBS    | 26        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Kava](https://github.com/kava-labs)                                       | KAVA   | 459       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Cosmos`                                                                      |
[Kobocoin](https://github.com/kobocoin/Kobocoin)                           | KOBO   | 196       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Komodo](https://github.com/KomodoPlatform/komodo)                         | KMD    | 141       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Landcoin](http://landcoin.co)                                             | LDCN   | 63        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[LBRY-Credits](https://github.com/lbryio/lbrycrd)                          | LBC    | 140       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Linx](https://github.com/linX-project/linX)                               | LINX   | 114       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Litecoin](https://github.com/litecoin-project/litecoin)                   | LTC    | 2         | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`, `P2WSH`, `P2WSH-In-P2SH`         |
[Litecoin-Cash](https://github.com/litecoincash-project/litecoincash)      | LCC    | 192       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[LitecoinZ](https://github.com/litecoinz-project/litecoinz)                | LTZ    | 221       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Lkrcoin](https://github.com/LKRcoin/lkrcoin)                              | LKR    | 557       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Lynx](https://github.com/doh9Xiet7weesh9va9th/lynx)                       | LYNX   | 191       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Mazacoin](https://github.com/MazaCoin/maza)                               | MZC    | 13        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Megacoin](https://github.com/LIMXTEC/Megacoin)                            | MEC    | 217       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Metis](https://github.com/MetisProtocol/metis)                            | METIS  | 60        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Ethereum`                                                                    |
[Minexcoin](https://github.com/minexcoin/minexcoin)                        | MNX    | 182       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Monacoin](https://github.com/monacoinproject/monacoin)                    | MONA   | 22        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`                                   |
[Monero](https://github.com/monero-project/monero)                         | XMR    | 128       | `mainnet`, `stagenet`, `testnet` | SLIP10-Ed25519-Monero  | `Monero`                                                                            | :x:                | `Monero`                                                                      |
[Monk](https://github.com/decenomy/MONK)                                   | MONK   | 214       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`                                   |
[MultiversX](https://github.com/multiversx/mx-chain-go)                    | EGLD   | 508       | `mainnet`                        | SLIP10-Ed25519         | `BIP44`, `BIP32`                                                                    | :x:                | `MultiversX`                                                                  |
[Myriadcoin](https://github.com/myriadteam/myriadcoin)                     | XMY    | 90        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Namecoin](https://github.com/namecoin/namecoin-core)                      | NMC    | 7         | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Nano](https://github.com/nanocurrency/nano-node)                          | XNO    | 165       | `mainnet`                        | SLIP10-Ed25519-Blake2b | `BIP44`, `BIP32`                                                                    | :x:                | `Nano`                                                                        |
[Navcoin](https://github.com/navcoin/navcoin-core)                         | NAV    | 130       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Near](https://github.com/near/nearcore)                                   | NEAR   | 397       | `mainnet`                        | SLIP10-Ed25519         | `BIP44`, `BIP32`                                                                    | :x:                | `Near`                                                                        |
[Neblio](https://github.com/NeblioTeam/neblio)                             | NEBL   | 146       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Neo](https://github.com/neo-project/neo)                                  | NEO    | 888       | `mainnet`                        | SLIP10-Nist256p1       | `BIP44`, `BIP32`                                                                    | :x:                | `Neo`                                                                         |
[Neoscoin](http://www.getneos.com)                                         | NEOS   | 25        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Neurocoin](https://github.com/neurocoin/neurocoin)                        | NRO    | 110       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[New-York-Coin](https://github.com/NewYorkCoinNYC/newyorkcoin)             | NYC    | 179       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Nine-Chronicles](https://github.com/planetarium/NineChronicles)           | NCG    | 567       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Ethereum`                                                                    |
[NIX](https://github.com/NixPlatform/NixCore)                              | NIX    | 400       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`                                   |
[Novacoin](https://github.com/novacoin-project/novacoin)                   | NVC    | 50        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[NuBits](https://bitbucket.org/NuNetwork/nubits)                           | NBT    | 12        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[NuShares](https://bitbucket.org/JordanLeePeershares/nubit/overview)       | NSR    | 11        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[OK-Cash](https://github.com/okcashpro/okcash)                             | OK     | 69        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[OKT-Chain](https://github.com/okex/okexchain)                             | OKT    | 996       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `OKT-Chain`                                                                   |
[Omni](https://github.com/omnilayer/omnicore)                              | OMNI   | 200       | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Onix](https://github.com/onix-project)                                    | ONX    | 174       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Ontology](https://github.com/ontio/ontology)                              | ONT    | 1024      | `mainnet`                        | SLIP10-Nist256p1       | `BIP44`, `BIP32`                                                                    | :x:                | `Neo`                                                                         |
[Optimism](https://github.com/ethereum-optimism)                           | OP     | 60        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Ethereum`                                                                    |
[Osmosis](https://github.com/osmosis-labs/osmosis)                         | OSMO   | 118       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Cosmos`                                                                      |
[Particl](https://github.com/particl/particl-core)                         | PART   | 44        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Peercoin](https://github.com/peercoin/peercoin)                           | PPC    | 6         | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Pesobit](https://github.com/pesobitph/pesobit-source)                     | PSB    | 62        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Phore](https://github.com/phoreproject/Phore)                             | PHR    | 444       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Pi-Network](https://github.com/pi-apps)                                   | PI     | 314159    | `mainnet`                        | SLIP10-Ed25519         | `BIP44`, `BIP32`                                                                    | :x:                | `Stellar`                                                                     |
[Pinkcoin](https://github.com/Pink2Dev/Pink2)                              | PINK   | 117       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Pivx](https://github.com/PIVX-Project/PIVX)                               | PIVX   | 119       | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Polygon](https://github.com/maticnetwork/whitepaper)                      | MATIC  | 60        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Ethereum`                                                                    |
[PoSW-Coin](https://posw.io)                                               | POSW   | 47        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Potcoin](https://github.com/potcoin/Potcoin)                              | POT    | 81        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Project-Coin](https://github.com/projectcoincore/ProjectCoin)             | PRJ    | 533       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Putincoin](https://github.com/PutinCoinPUT/PutinCoin)                     | PUT    | 122       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Qtum](https://github.com/qtumproject/qtum)                                | QTUM   | 2301      | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP84`, `BIP141`, `BIP32`, `BIP86`, `BIP44`, `BIP49`                               | :white_check_mark: | `P2PKH`, `P2SH`, `P2TR`, `P2WPKH`, `P2WPKH-In-P2SH`, `P2WSH`, `P2WSH-In-P2SH` |
[Rapids](https://github.com/RapidsOfficial/Rapids)                         | RPD    | 320       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Ravencoin](https://github.com/RavenProject/Ravencoin)                     | RVN    | 175       | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP32`, `BIP44`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`, `P2WSH`, `P2WSH-In-P2SH`         |
[Reddcoin](https://github.com/reddcoin-project/reddcoin)                   | RDD    | 4         | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Ripple](https://github.com/ripple/rippled)                                | XRP    | 144       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Ritocoin](https://github.com/RitoProject/Ritocoin)                        | RITO   | 19169     | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[RSK](https://github.com/rsksmart)                                         | RBTC   | 137       | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Rubycoin](https://github.com/rubycoinorg/rubycoin)                        | RBY    | 16        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Safecoin](https://github.com/Fair-Exchange/safecoin)                      | SAFE   | 19165     | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Saluscoin](https://github.com/saluscoin/SaluS)                            | SLS    | 572       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Scribe](https://github.com/scribenetwork/scribe)                          | SCRIBE | 545       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Secret](https://github.com/scrtlabs/SecretNetwork)                        | SCRT   | 529       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Cosmos`                                                                      |
[Shadow-Cash](https://github.com/shadowproject/shadow)                     | SDC    | 35        | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Shentu](https://github.com/ShentuChain)                                   | CTK    | 118       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Cosmos`                                                                      |
[Slimcoin](https://github.com/slimcoin-project/Slimcoin)                   | SLM    | 63        | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Smileycoin](https://github.com/tutor-web/)                                | SMLY   | 59        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Solana](https://github.com/solana-labs/solana)                            | SOL    | 501       | `mainnet`                        | SLIP10-Ed25519         | `BIP44`, `BIP32`                                                                    | :x:                | `Solana`                                                                      |
[Solarcoin](https://github.com/onsightit/solarcoin)                        | SLR    | 58        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Stafi](https://github.com/stafiprotocol/stafi-node)                       | FIS    | 907       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Cosmos`                                                                      |
[Stash](https://docs.stash.capital)                                        | STASH  | 49344     | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Stellar](https://github.com/stellar/stellar-core)                         | XLM    | 148       | `mainnet`                        | SLIP10-Ed25519         | `BIP44`, `BIP32`                                                                    | :x:                | `Stellar`                                                                     |
[Stratis](https://github.com/stratisproject)                               | STRAT  | 105       | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Sugarchain](https://github.com/sugarchain-project/sugarchain)             | SUGAR  | 408       | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`                                   |
[Sui](https://github.com/MystenLabs/sui)                                   | SUI    | 784       | `mainnet`                        | SLIP10-Ed25519         | `BIP44`, `BIP32`                                                                    | :x:                | `Sui`                                                                         |
[Syscoin](https://github.com/syscoin/syscoin)                              | SYS    | 57        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`                                   |
[Terra](https://github.com/terra-money/core)                               | LUNA   | 330       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Cosmos`                                                                      |
[Tezos](https://github.com/tezos/tezos)                                    | XTZ    | 1729      | `mainnet`                        | SLIP10-Ed25519         | `BIP44`, `BIP32`                                                                    | :x:                | `Tezos`                                                                       |
[Theta](https://github.com/thetatoken)                                     | THETA  | 500       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Ethereum`                                                                    |
[Thought-AI](https://github.com/thoughtnetwork)                            | THT    | 502       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[TOA-Coin](https://github.com/toacoin/TOA)                                 | TOA    | 159       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Tron](https://github.com/tronprotocol/java-tron)                          | TRX    | 195       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `P2PKH`, `P2SH`                                                               |
[TWINS](https://github.com/NewCapital/TWINS-Core)                          | TWINS  | 970       | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Ultimate-Secure-Cash](https://github.com/SilentTrader/UltimateSecureCash) | USC    | 112       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Unobtanium](https://github.com/unobtanium-official/Unobtanium)            | UNO    | 92        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Vcash](https://vcash.finance)                                             | VC     | 127       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[VeChain](https://github.com/vechain)                                      | VET    | 818       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Ethereum`                                                                    |
[Verge](https://github.com/vergecurrency/verge)                            | XVG    | 77        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Vertcoin](https://github.com/vertcoin/vertcoin)                           | VTC    | 28        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`                                   |
[Viacoin](https://github.com/viacoin/viacoin)                              | VIA    | 14        | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`, `P2WPKH`, `P2WPKH-In-P2SH`                                   |
[Vivo](https://github.com/vivocoin/vivo)                                   | VIVO   | 166       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Voxels](http://revolutionvr.live)                                         | VOX    | 129       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Virtual-Cash](https://github.com/Bit-Net/vash)                            | VASH   | 33        | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Wagerr](https://github.com/wagerr/wagerr)                                 | WGR    | 0         | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Whitecoin](https://github.com/Whitecoin-XWC/Whitecoin-core)               | XWC    | 559       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Wincoin](https://github.com/Wincoinofficial/wincoin)                      | WC     | 181       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[XinFin](https://github.com/XinFinOrg/XDPoSChain)                          | XDC    | 550       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `XinFin`                                                                      |
[XUEZ](https://github.com/XUEZ/Xuez-Core)                                  | XUEZ   | 225       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Ycash](https://github.com/ycashfoundation/ycash)                          | YEC    | 347       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Zcash](https://github.com/zcash/zcash)                                    | ZEC    | 133       | `mainnet`, `testnet`             | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[ZClassic](https://github.com/ZClassicCommunity/zclassic)                  | ZCL    | 147       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Zetacoin](https://github.com/zetacoin/zetacoin)                           | ZET    | 719       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |
[Zilliqa](https://github.com/Zilliqa/Zilliqa)                              | ZIL    | 313       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :x:                | `Zilliqa`                                                                     |
[ZooBC](https://github.com/zoobc/zoobc-core)                               | ZBC    | 883       | `mainnet`                        | SLIP10-Secp256k1       | `BIP44`, `BIP32`                                                                    | :white_check_mark: | `P2PKH`, `P2SH`                                                               |

## Donations

If You found this tool helpful consider making a donation:

| Coins                         | Addresses                                  |
| ----------------------------- | :----------------------------------------: |
| Bitcoin `BTC`                 | 3GGNPvgbSpMHShcaZJGDXQn5wUJyTz7uoC         |
| Ethereum `ETH`, Tether `USDT` | 0x342798bbe9731a91e0557fa8ab0bce1eae6d6ae3 |

## License

Distributed under the [MIT](https://github.com/meherett/python-hdwallet/blob/master/LICENSE) license. See ``LICENSE`` for more information.
