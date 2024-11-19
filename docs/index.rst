=================================
Hierarchical Deterministic Wallet
=================================

|Build Status| |PyPI Version| |Documentation Status| |PyPI License| |PyPI Python Version| |Coverage Status|

.. |Build Status| image:: https://travis-ci.org/talonlab/python-hdwallet.svg?branch=master
   :target: https://travis-ci.org/talonlab/python-hdwallet?branch=master

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

For more info see the BIP specs.

.. list-table::
   :widths: 10 185
   :header-rows: 1

   * - BIP's
     - Titles
   * - `BIP39 <https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki>`_
     - Mnemonic code for generating deterministic keys
   * - `BIP85 <https://github.com/bitcoin/bips/blob/master/bip-0085.mediawiki>`_
     - Deterministic Entropy From BIP32 Keychains
   * - `BIP32 <https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki>`_
     - Hierarchical Deterministic Wallets
   * - `BIP44 <https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki>`_
     - Multi-Account Hierarchy for Deterministic Wallets
   * - `BIP49 <https://github.com/bitcoin/bips/blob/master/bip-0049.mediawiki>`_
     - Derivation scheme for P2WPKH-nested-in-P2SH based accounts
   * - `BIP84 <https://github.com/bitcoin/bips/blob/master/bip-0084.mediawiki>`_
     - Derivation scheme for P2WPKH based accounts
   * - `BIP141 <https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki>`_
     - Segregated Witness (Consensus layer)
