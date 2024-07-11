:orphan:

=========
Entropies
=========

A measure of randomness or unpredictability in a system.
It is essential for generating secure cryptographic keys, ensuring
they are difficult to guess or reproduce by attackers.

.. autoclass:: hdwallet.entropies.ENTROPIES
    :members:

>>> from hdwallet.entropies import ENTROPIES
>>> ENTROPIES.names()
['Algorand', 'BIP39', 'Electrum-V1', 'Electrum-V2', 'Monero']
>>> ENTROPIES.classes()
[<class 'hdwallet.entropies.algorand.AlgorandEntropy'>, <class 'hdwallet.entropies.bip39.BIP39Entropy'>, <class 'hdwallet.entropies.electrum.v1.ElectrumV1Entropy'>, <class 'hdwallet.entropies.electrum.v2.ElectrumV2Entropy'>, <class 'hdwallet.entropies.monero.MoneroEntropy'>]
>>> from hdwallet.entropies import BIP39Entropy
>>> ENTROPIES.entropy(name="BIP39")
<class 'hdwallet.entropies.bip39.BIP39Entropy'>
>>> ENTROPIES.entropy(name="BIP39") == BIP39Entropy
True
>>> ENTROPIES.is_entropy(name="Electrum-V2")
True

.. autoclass:: hdwallet.entropies.ientropy.IEntropy
    :members:

.. autoclass:: hdwallet.entropies.algorand.AlgorandEntropy
    :members:

.. autoclass:: hdwallet.entropies.bip39.BIP39Entropy
    :members:

>>> from hdwallet.entropies.bip39 import BIP39Entropy, BIP39_ENTROPY_STRENGTHS
>>> entropy: str = BIP39Entropy.generate(
    strength=BIP39_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT
)
>>> entropy
"89f89c8d5445f37dde5d70212bf3f6b4"
>>> bip39_entropy: BIP39Entropy = BIP39Entropy(entropy=entropy)
>>> bip39_entropy.name()
"BIP39"
>>> bip39_entropy.entropy()
"89f89c8d5445f37dde5d70212bf3f6b4"
>>> bip39_entropy.strength()
128

.. autoclass:: hdwallet.entropies.electrum.v1.ElectrumV1Entropy
    :members:

.. autoclass:: hdwallet.entropies.electrum.v2.ElectrumV2Entropy
    :members:

.. autoclass:: hdwallet.entropies.monero.MoneroEntropy
    :members:

