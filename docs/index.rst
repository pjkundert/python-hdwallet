=================================
Hierarchical Deterministic Wallet
=================================

|Build Status| |PyPI Version| |Documentation Status| |PyPI License| |PyPI Python Version| |Coverage Status|

.. |Build Status| image:: https://img.shields.io/github/actions/workflow/status/talonlab/python-hdwallet/build.yml
   :target: https://github.com/talonlab/python-hdwallet/actions/workflows/build.yml

.. |PyPI Version| image:: https://img.shields.io/pypi/v/hdwallet.svg?color=blue
   :target: https://pypi.org/project/hdwallet

.. |Documentation Status| image:: https://readthedocs.org/projects/hdwallet/badge/?version=master
   :target: https://hdwallet.readthedocs.io/en/master/?badge=master

.. |PyPI License| image:: https://img.shields.io/pypi/l/hdwallet?color=black
   :target: https://pypi.org/project/hdwallet

.. |PyPI Python Version| image:: https://img.shields.io/pypi/pyversions/hdwallet.svg
   :target: https://pypi.org/project/hdwallet

.. |Coverage Status| image:: https://coveralls.io/repos/github/talonlab/python-hdwallet/badge.svg?branch=master
   :target: https://coveralls.io/github/talonlab/python-hdwallet?branch=master

Python-based library for the implementation of a Hierarchical Deterministic (HD) Wallet generator supporting more than 200 cryptocurrencies.
It allows the handling of multiple coins, multiple accounts, external and internal chains per account, and millions of addresses per chain.

.. epigraph::

   The library is designed to be flexible and scalable, making it ideal for developers who need to integrate multi-currency wallet functionalities into their applications.
   It supports standard protocols for compatibility with other wallets and services, offering features like secure seed creation, efficient key management, and easy account handling.

   This library simplifies the complexity of blockchain interactions and enhances security for end-users.

.. list-table::
   :widths: 30 200
   :header-rows: 1

   * - Components
     - Protocols
   * - Cryptocurrencies
     - `#supported-cryptocurrencies <cryptocurrencies.html>`_
   * - Entropies
     - ``Algorand``, ``BIP39``, ``Electrum-V1``, ``Electrum-V2``, ``Monero``
   * - Mnemonics
     - ``Algorand``, ``BIP39``, ``Electrum-V1``, ``Electrum-V2``, ``Monero``
   * - Seeds
     - ``Algorand``, ``BIP39``, ``Cardano``, ``Electrum-V1``, ``Electrum-V2``, ``Monero``
   * - Elliptic Curve Cryptography's
     - ``Kholaw-Ed25519``, ``SLIP10-Ed25519``, ``SLIP10-Ed25519-Blake2b``, ``SLIP10-Ed25519-Monero``, ``SLIP10-Nist256p1``, ``SLIP10-Secp256k1``
   * - Hierarchical Deterministic's
     - ``BIP32``, ``BIP44``, ``BIP49``, ``BIP84``, ``BIP86``, ``BIP141``, ``Cardano``, ``Electrum-V1``, ``Electrum-V2``, ``Monero``
   * - Derivations
     - ``BIP44``, ``BIP49``, ``BIP84``, ``BIP86``, ``CIP1852``, ``Custom``, ``Electrum``, ``Monero``, ``HDW (Our own custom derivation)``
   * - Addresses
     - ``Algorand``, ``Aptos``, ``Avalanche``, ``Cardano``, ``Cosmos``, ``EOS``, ``Ergo``, ``Ethereum``, ``Filecoin``, ``Harmony``, ``Icon``, ``Injective``, ``Monero``, ``MultiversX``, ``Nano``, ``Near``, ``Neo``, ``OKT-Chain``, ``P2PKH``, ``P2SH``, ``P2TR``, ``P2WPKH``, ``P2WPKH-In-P2SH``, ``P2WSH``, ``P2WSH-In-P2SH``, ``Ripple``, ``Solana``, ``Stellar``, ``Sui``, ``Tezos``, ``Tron``, ``XinFin``, ``Zilliqa``
   * - Others
     - ``BIP38``, ``Wallet Import Format``, ``Serialization``
