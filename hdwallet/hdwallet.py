#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Optional, Union, Any, Type, Literal, Tuple, Dict, List
)

import struct

from .libs.base58 import (
    check_encode, checksum_encode, check_decode, ensure_string
)
from .entropies import (
    IEntropy, ENTROPIES, AlgorandEntropy, BIP39Entropy, ElectrumV1Entropy, ElectrumV2Entropy, MoneroEntropy
)
from .mnemonics import (
    IMnemonic, MNEMONICS, AlgorandMnemonic, BIP39Mnemonic, ElectrumV1Mnemonic, ElectrumV2Mnemonic, MoneroMnemonic
)
from .seeds import (
    ISeed, SEEDS, AlgorandSeed, BIP39Seed, CardanoSeed, ElectrumV1Seed, ElectrumV2Seed, MoneroSeed
)
from .ecc import (
    SLIP10Ed25519MoneroPrivateKey, SLIP10Ed25519MoneroPublicKey
)
from .hds import (
    IHD, HDS
)
from .hds.electrum.v2 import ELECTRUM_V2_MODES
from .cryptocurrencies.icryptocurrency import (
    ICryptocurrency, INetwork
)
from .addresses import ADDRESSES
from .keys import (
    serialize, deserialize
)
from .exceptions import (
    DerivationError, NetworkError, SymbolError, AddressError, SemanticError
)
from .utils import (
    get_bytes, bytes_to_integer, integer_to_bytes, bytes_to_string
)
from .derivations import (
    IDerivation, CustomDerivation, BIP44Derivation, BIP49Derivation, BIP84Derivation, BIP86Derivation, CIP1852Derivation, ElectrumDerivation
)
from .wif import WIF_TYPES
from .addresses import IAddress


class HDWallet:

    _cryptocurrency: ICryptocurrency
    _network: INetwork
    _address: Type[IAddress]

    _entropy: Optional[IEntropy] = None
    _language: Optional[str] = None
    _passphrase: Optional[str] = None
    _mnemonic: Optional[IMnemonic] = None
    _seed: Optional[ISeed] = None
    _derivation: Optional[IDerivation] = None

    _semantic: Optional[str] = None

    _mode: Optional[str] = None  # "standard" or "segwit"
    _public_key_type: Optional[str] = None  # "uncompressed" or "compressed"
    _cardano_type: Optional[str] = None
    _use_default_path: bool = True

    _hd: IHD

    def __init__(
        self,
        cryptocurrency: Type[ICryptocurrency],
        hd: Optional[Type[IHD]] = None,
        network: Union[str, Type[INetwork]] = "mainnet",
        address: Optional[Union[str, Type[IAddress]]] = None,
        **kwargs
    ) -> None:

        if not issubclass(cryptocurrency, ICryptocurrency):
            raise Exception("Invalid cryptocurrency class")
        self._cryptocurrency = cryptocurrency()

        if hd is None:  # Use default hd
            hd = HDS[self._cryptocurrency.DEFAULT_HD]
        elif hd is not None and not issubclass(hd, IHD):
            raise Exception("Invalid Hierarchical Deterministic (HD) instance")
        if hd.name() in ["BIP32", "BIP44", "BIP49", "BIP84", "BIP84", "BIP141", "Electrum-V1"]:
            if not kwargs.get("public_key_type") and hd.name() == "Electrum-V1":
                self._public_key_type = kwargs.get("public_key_type", "uncompressed")
            elif not kwargs.get("public_key_type") and hd.name() != "Electrum-V1":
                self._public_key_type = kwargs.get("public_key_type", "compressed")
            elif kwargs.get("public_key_type") in ["uncompressed", "compressed"]:
                self._public_key_type = kwargs.get("public_key_type")
            else:
                raise ValueError("Invalid public key type, choose only 'uncompressed' or 'compressed' types")
        elif hd.name() == "Cardano":
            from .cryptocurrencies import Cardano
            if not kwargs.get("cardano_type"):
                self._cardano_type = kwargs.get("cardano_type", "shelley-icarus")
            elif Cardano.TYPES.is_cardano_type(kwargs.get("cardano_type")):
                self._cardano_type = kwargs.get("cardano_type")
            else:
                raise ValueError("Invalid Cardano type")
        elif hd.name() == "Electrum-V2":
            if not kwargs.get("mode"):
                self._mode = kwargs.get("mode", "standard")  # Default
            elif kwargs.get("mode") in ELECTRUM_V2_MODES.get_modes():
                self._mode = kwargs.get("mode")
            else:
                raise ValueError(f"Invalid Electrum V2 mode, (expected: 'standard' or 'segwit', got: '{kwargs.get('mode')}')")

        try:
            if not isinstance(network, str) and issubclass(network, INetwork):
                network = network.__name__.lower()
            if not self._cryptocurrency.NETWORKS.is_network(network=network):
                raise NetworkError(
                    f"Wrong {self._cryptocurrency.NAME} network",
                    expected=self._cryptocurrency.NETWORKS.get_networks(),
                    got=network
                )
            self._network = self._cryptocurrency.NETWORKS.get_network(network=network)
        except TypeError:
            raise NetworkError(
                "Invalid network type", expected=[str, INetwork], got=type(network)
            )

        if address is None:  # Use default address
            address = self._cryptocurrency.DEFAULT_ADDRESS
        elif issubclass(address, IAddress):
            address = address.name()
        if address not in self._cryptocurrency.ADDRESSES.get_addresses():
            raise AddressError(
                f"Wrong {self._cryptocurrency.NAME} address",
                expected=self._cryptocurrency.ADDRESSES.get_addresses(),
                got=address
            )
        self._address = ADDRESSES[address]

        if hd.name() not in cryptocurrency.HDS.get_hds():
            raise Exception(f"{hd.name()} HD not implemented on {cryptocurrency.NAME} cryptocurrency")

        if hd.name() in ["BIP32", "BIP44", "BIP49", "BIP84", "BIP86", "BIP141"]:
            self._hd = hd(ecc_name=cryptocurrency.ECC.NAME, public_key_type=self._public_key_type)
        elif hd.name() == "Cardano":
            self._hd = hd(cardano_type=self._cardano_type)
        elif hd.name() == "Electrum-V1":
            self._hd = hd(public_key_type=self._public_key_type)
        elif hd.name() == "Electrum-V2":
            self._hd = hd(mode=self._mode, public_key_type=self._public_key_type)
        elif hd.name() == "Monero":
            self._hd = hd(network=self._network.__name__.lower())

        self._language = kwargs.get("language", "english")
        self._passphrase = kwargs.get("passphrase", None)
        self._use_default_path = kwargs.get("use_default_path", False)
        # self._cryptocurrency.get_default_path(network=self._network.__name__.lower())

    def from_entropy(self, entropy: IEntropy, **kwargs) -> "HDWallet":

        if entropy.name() not in self._cryptocurrency.ENTROPIES.get_entropies():
            raise Exception(f"Invalid entropy class for {self._cryptocurrency.NAME} cryptocurrency")
        self._entropy = entropy

        mnemonic: str = MNEMONICS[self._entropy.name()].from_entropy(
            entropy=self._entropy.entropy(), language=self._language, kwargs=kwargs
        )
        return self.from_mnemonic(
            mnemonic=MNEMONICS[self._entropy.name()](mnemonic=mnemonic)
        )

    def from_mnemonic(self, mnemonic: IMnemonic) -> "HDWallet":

        if mnemonic.name() not in self._cryptocurrency.MNEMONICS.get_mnemonics():
            raise Exception(f"Invalid mnemonic class for {self._cryptocurrency.NAME} cryptocurrency")
        self._mnemonic = mnemonic

        self._entropy = ENTROPIES[self._mnemonic.name()](
            entropy=self._mnemonic.decode(
                mnemonic=self._mnemonic.mnemonic()
            )
        )
        seed: str = SEEDS[self._mnemonic.name()].generate(
            mnemonic=self._mnemonic.mnemonic(), passphrase=self.passphrase()
        )
        return self.from_seed(
            seed=SEEDS[self._mnemonic.name()](seed=seed)
        )

    def from_seed(self, seed: ISeed) -> "HDWallet":

        if seed.name() not in self._cryptocurrency.SEEDS.get_seeds():
            raise Exception(f"Invalid seed class for {self._cryptocurrency.NAME} cryptocurrency")
        self._seed = seed

        self._hd.from_seed(
            seed=seed.seed(), passphrase=self.passphrase()
        )
        return self

    def from_xprivate_key(self, xprivate_key: str, encoded: bool = True) -> "HDWallet":

        if self._hd.name() in ["Electrum-V1", "Monero"]:
            raise NotImplementedError(f"Conversion from xprivate key is not implemented for the {self._hd.name()} HD type")

        version, depth, parent_fingerprint, index, chain_code, key = deserialize(
            key=xprivate_key, encoded=encoded
        )

        if not self._network.XPRIVATE_KEY_VERSIONS.is_version(version=version) or \
                len(check_decode(xprivate_key) if encoded else xprivate_key) not in [78, 110]:
            raise Exception(f"Invalid {self._cryptocurrency.NAME} extended(x) private key")

        self._hd.from_xprivate_key(
            xprivate_key=xprivate_key, encoded=encoded
        )
        return self

    def from_xpublic_key(self, xpublic_key: str, encoded: bool = True) -> "HDWallet":

        if self._hd.name() in ["Electrum-V1", "Monero"]:
            raise NotImplementedError(f"Conversion from xpublic key is not implemented for the {self._hd.name()} HD type")

        version, depth, parent_fingerprint, index, chain_code, key = deserialize(
            key=xpublic_key, encoded=encoded
        )

        if not self._network.XPUBLIC_KEY_VERSIONS.is_version(version=version) or \
                len(check_decode(xpublic_key) if encoded else xpublic_key) not in [78, 110]:
            raise Exception(f"Invalid {self._cryptocurrency.NAME} extended(x) public key")

        self._hd.from_xpublic_key(
            xpublic_key=xpublic_key, encoded=encoded
        )
        return self

    def from_derivation(self, derivation: IDerivation) -> "HDWallet":
        if self._hd.name() in ["Electrum-V1", "Monero"]:
            raise NotImplementedError(f"from_derivation is not implemented for the {self._hd.name()} HD type")
        self._hd.from_derivation(derivation=derivation)
        self._derivation = derivation
        return self

    def update_derivation(self, derivation: IDerivation) -> "HDWallet":
        if self._hd.name() in ["Monero"]:
            raise NotImplementedError(f"update_derivation is not implemented for the {self._hd.name()} HD type")
        self._hd.update_derivation(derivation=derivation)
        self._derivation = derivation
        return self

    def clean_derivation(self) -> "HDWallet":
        if self._hd.name() in ["Electrum-V1", "Monero"]:
            raise NotImplementedError(f"clean_derivation is not implemented for the {self._hd.name()} HD type")
        self._hd.clean_derivation()
        self._derivation = None
        return self

    def from_private_key(self, private_key: str) -> "HDWallet":
        self._hd.from_private_key(private_key=private_key)
        return self

    def from_wif(self, wif: str) -> "HDWallet":
        if self._hd.name() in ["Cardano", "Monero"]:
            raise NotImplementedError(f"Wallet Important Format (WIF) is not supported by {self._hd.name()} HD wallet's")

        self._hd.from_wif(wif=wif)
        return self

    def from_public_key(self, public_key: str) -> "HDWallet":
        if self._hd.name() in ["Monero"]:
            raise NotImplementedError(f"from_public_key is not implemented for the {self._hd.name()} HD type")
        self._hd.from_public_key(public_key=public_key)
        return self

    def from_spend_private_key(self, spend_private_key: Union[bytes, str, SLIP10Ed25519MoneroPrivateKey]) -> "HDWallet":
        if self._hd.name() != "Monero":
            raise NotImplementedError("From spend private key only supported by Monero HD wallet")
        self._hd.from_spend_private_key(spend_private_key=spend_private_key)
        return self

    def from_watch_only(
        self, view_private_key: Union[bytes, str, SLIP10Ed25519MoneroPrivateKey], spend_public_key: Union[bytes, str, SLIP10Ed25519MoneroPublicKey]
    ) -> "HDWallet":
        if self._hd.name() != "Monero":
            raise NotImplementedError("From spend watch only supported by Monero HD wallet")
        self._hd.from_watch_only(
            view_private_key=view_private_key, spend_public_key=spend_public_key
        )
        return self

    def cryptocurrency(self) -> str:
        return self._cryptocurrency.NAME

    def symbol(self) -> str:
        return self._cryptocurrency.SYMBOL

    def network(self) -> str:
        return self._network.__name__.lower()

    def entropy(self) -> Optional[str]:
        return self._entropy.entropy() if self._entropy else None

    def strength(self) -> Optional[str]:
        return self._entropy.strength() if self._entropy else None

    def mnemonic(self) -> Optional[str]:
        return self._mnemonic.mnemonic() if self._mnemonic else None

    def passphrase(self) -> Optional[str]:
        return self._passphrase if self._passphrase else None

    def language(self) -> Optional[str]:
        return self._mnemonic.language() if self._mnemonic else None

    def seed(self) -> Optional[str]:
        return self._hd.seed()

    def ecc(self) -> str:
        return self._cryptocurrency.ECC.NAME

    def mode(self) -> str:

        if self._hd.name() not in ["Electrum-V2"]:
            raise NotImplementedError(f"Get mode is only for {self._hd.name()} HD type")

        return self._hd.mode()

    def path_key(self) -> Optional[str]:
        return self._hd.path_key()

    def root_xprivate_key(self, semantic: str = "P2PKH", encoded: bool = True) -> Optional[str]:

        if self._hd.name() in ["Electrum-V1", "Monero"]:
            raise NotImplementedError(f"Conversion from xprivate key is not implemented for the {self._hd.name()} HD type")

        return self._hd.root_xprivate_key(
            version=self._network.XPRIVATE_KEY_VERSIONS.get_version(semantic), encoded=encoded
        )

    def root_xpublic_key(self, semantic: str = "P2PKH", encoded: bool = True) -> Optional[str]:

        if self._hd.name() in ["Electrum-V1", "Monero"]:
            raise NotImplementedError(f"Conversion from xpublic key is not implemented for the {self._hd.name()} HD type")

        return self._hd.root_xpublic_key(
            version=self._network.XPUBLIC_KEY_VERSIONS.get_version(semantic), encoded=encoded
        )

    def master_xprivate_key(self, semantic: str = "P2PKH", encoded: bool = True) -> Optional[str]:
        return self.root_xprivate_key(semantic=semantic, encoded=encoded)

    def master_xpublic_key(self, semantic: str = "P2PKH", encoded: bool = True) -> Optional[str]:
        return self.root_xpublic_key(semantic=semantic, encoded=encoded)

    def root_private_key(self) -> Optional[str]:
        if self._hd.name() == "Electrum-V1":
            return self._hd.master_private_key()
        return self._hd.root_private_key()

    def root_chain_code(self) -> Optional[str]:
        return self._hd.root_chain_code()

    def root_public_key(self, public_key_type: Optional[str] = None) -> Optional[str]:
        if self._hd.name() == "Electrum-V1":
            return self._hd.master_public_key(public_key_type=public_key_type)
        return self._hd.root_public_key(public_key_type=public_key_type)

    def master_private_key(self) -> Optional[str]:
        if self._hd.name() == "Electrum-V1":
            return self._hd.master_private_key()
        return self._hd.root_private_key()

    def master_chain_code(self) -> Optional[str]:
        return self._hd.root_chain_code()

    def master_public_key(self, public_key_type: Optional[str] = None) -> Optional[str]:
        if self._hd.name() == "Electrum-V1":
            return self._hd.master_public_key(public_key_type=public_key_type)
        return self._hd.root_public_key(public_key_type=public_key_type)

    def xprivate_key(self, semantic: str = "P2PKH", encoded: bool = True) -> Optional[str]:

        if self._hd.name() in ["Electrum-V1", "Monero"]:
            raise NotImplementedError(f"Conversion from xprivate key is not implemented for the {self._hd.name()} HD type")

        return self._hd.xprivate_key(
            version=self._network.XPRIVATE_KEY_VERSIONS.get_version(semantic), encoded=encoded
        )

    def xpublic_key(self, semantic: str = "P2PKH", encoded: bool = True) -> Optional[str]:

        if self._hd.name() in ["Electrum-V1", "Monero"]:
            raise NotImplementedError(f"Conversion from xpublic key is not implemented for the {self._hd.name()} HD type")

        return self._hd.xpublic_key(
            version=self._network.XPUBLIC_KEY_VERSIONS.get_version(semantic), encoded=encoded
        )

    def private_key(self) -> Optional[str]:
        return self._hd.private_key()

    def spend_private_key(self) -> str:
        if self._hd.name() != "Monero":
            raise NotImplementedError("Spend private key only supported by Monero HD wallet")
        return self._hd.spend_private_key()

    def view_private_key(self) -> str:
        if self._hd.name() != "Monero":
            raise NotImplementedError("View private key only supported by Monero HD wallet")
        return self._hd.view_private_key()

    def wif(self, wif_type: Optional[str] = None) -> Optional[str]:
        return self._hd.wif(wif_type=wif_type)

    def wif_type(self) -> str:
        return self._hd.wif_type()

    def chain_code(self) -> Optional[str]:
        return self._hd.chain_code()

    def public_key(self, public_key_type: Optional[str] = None) -> str:
        return self._hd.public_key(public_key_type=public_key_type)

    def public_key_type(self) -> str:
        return self._hd.public_key_type()

    def uncompressed(self) -> str:
        return self._hd.uncompressed()

    def compressed(self) -> str:
        return self._hd.compressed()

    def spend_public_key(self) -> str:
        if self._hd.name() != "Monero":
            raise NotImplementedError("Spend public key only supported by Monero HD wallet")
        return self._hd.spend_public_key()

    def view_public_key(self) -> str:
        if self._hd.name() != "Monero":
            raise NotImplementedError("view public key only supported by Monero HD wallet")
        return self._hd.view_public_key()

    def hash(self) -> str:
        return self._hd.hash()

    def depth(self) -> int:
        return self._hd.depth()

    def fingerprint(self) -> str:
        return self._hd.fingerprint()

    def parent_fingerprint(self) -> str:
        return self._hd.parent_fingerprint()

    def path(self) -> str:
        return self._hd.path()

    def index(self) -> int:
        return self._hd.index()

    def indexes(self) -> List[int]:
        return self._hd.indexes()

    def primary_address(self) -> Optional[str]:
        if self._hd.name() == "Monero":
            return self._hd.primary_address()

    def integrated_address(self, payment_id: Union[bytes, str]) -> Optional[str]:
        if self._hd.name() == "Monero":
            return self._hd.integrated_address(payment_id=payment_id)

    def sub_address(self, minor_index: int, major_index: int = 0) -> Optional[str]:
        if self._hd.name() == "Monero":
            return self._hd.sub_address(
                minor_index=minor_index, major_index=major_index
            )

    def address(self, address: Optional[Union[str, Type[IAddress]]] = None, **kwargs) -> str:

        if address is None:
            address = self._address.name()
        elif issubclass(address, IAddress):
            address = address.name()
        if address not in self._cryptocurrency.ADDRESSES.get_addresses():
            raise AddressError(
                f"Wrong {self._cryptocurrency.NAME} address",
                expected=self._cryptocurrency.ADDRESSES.get_addresses(),
                got=address
            )

        if self._cryptocurrency.NAME in [
            "Algorand", "Elrond", "Solana", "Stellar", "Tezos"
        ]:
            return ADDRESSES[address].encode(
                public_key=self.public_key(), **kwargs
            )
        elif self._cryptocurrency.NAME == "Cardano":
            return self._hd.address(
                network=self._network.__name__.lower(), **kwargs
            )
        elif self._cryptocurrency.NAME == "Monero":
            if kwargs.get("version_type") == "standard":
                return self.primary_address()
            elif kwargs.get("version_type") == "integrated":
                return self.integrated_address(
                    payment_id=get_bytes(kwargs.get("payment_id"))
                )
            elif kwargs.get("version_type") == "sub-address":
                return self.sub_address(
                    minor_index=kwargs.get("minor_index"), major_index=kwargs.get("major_index", 0)
                )
        elif self._cryptocurrency.NAME in [
            "Bitcoin"
        ]:
            if address == "P2PKH":
                return ADDRESSES[address].encode(
                    public_key=self.public_key(),
                    network_version=self._network.PUBLIC_KEY_ADDRESS_PREFIX,
                    public_key_type=self.public_key_type()
                )
            elif address in ["P2SH", "P2WPKH-In-P2SH", "P2WSH-In-P2SH"]:
                return ADDRESSES[address].encode(
                    public_key=self.public_key(),
                    network_version=self._network.SCRIPT_ADDRESS_PREFIX,
                    public_key_type=self.public_key_type()
                )
            elif address == "P2TR":
                return ADDRESSES[address].encode(
                    public_key=self.public_key(),
                    hrp=self._network.HRP,
                    witness_version=self._network.WITNESS_VERSIONS.get_witness_version(address)
                )
            elif address in ["P2WPKH", "P2WSH"]:
                return ADDRESSES[address].encode(
                    public_key=self.public_key(),
                    hrp=self._network.HRP,
                    witness_version=self._network.WITNESS_VERSIONS.get_witness_version(address),
                    public_key_type=self.public_key_type()
                )

    def dump(self) -> dict:
        return dict(
            cryptocurrency=self.cryptocurrency(),
            symbol=self.symbol(),
            network=self.network(),
            entropy=self.entropy(),
            strength=self.strength(),
            mnemonic=self.mnemonic(),
            passphrase=self.passphrase(),
            language=self.language(),
            seed=self.seed(),
            root_xprivate_key=self.root_xprivate_key(),
            root_xpublic_key=self.root_xpublic_key(),
            root_private_key=self.root_private_key(),
            root_chain_code=self.root_chain_code(),
            root_public_key=self.root_public_key(),
            xprivate_key=self.xprivate_key(),
            xpublic_key=self.xpublic_key(),
            private_key=self.private_key(),
            chain_code=self.chain_code(),
            public_key=self.public_key(),
            uncompressed=self.uncompressed(),
            compressed=self.compressed(),
            hash=self.hash(),
            depth=self.depth(),
            path=self.path(),
            index=self.index(),
            indexes=self.indexes(),
            fingerprint=self.fingerprint(),
            parent_fingerprint=self.parent_fingerprint(),
            address=self.address()
        )

    def dumps(self, **kwargs) -> dict:

        dumps: dict = dict(
            cryptocurrency=self.cryptocurrency(),
            symbol=self.symbol(),
            network=self.network(),
            entropy=self.entropy(),
            strength=self.strength(),
            mnemonic=self.mnemonic(),
            passphrase=self.passphrase(),
            language=self.language(),
            seed=self.seed(),
            root_xprivate_key=self.root_xprivate_key(),
            root_xpublic_key=self.root_xpublic_key(),
            root_private_key=self.root_private_key(),
            root_chain_code=self.root_chain_code(),
            root_public_key=self.root_public_key()
        )

        def get_derivation() -> dict:
            return dict(
                xprivate_key=self.xprivate_key(),
                xpublic_key=self.xpublic_key(),
                private_key=self.private_key(),
                chain_code=self.chain_code(),
                public_key=self.public_key(),
                uncompressed=self.uncompressed(),
                compressed=self.compressed(),
                hash=self.hash(),
                depth=self.depth(),
                path=self.path(),
                index=self.index(),
                indexes=self.indexes(),
                fingerprint=self.fingerprint(),
                parent_fingerprint=self.parent_fingerprint(),
                address=self.address()
            )

        derivations: List[dict] = []
        if self._derivation.name() in ["BIP44", "BIP49", "BIP84", "BIP86", "CIP1852"]:
            from_account_index: int = kwargs.get("from_account_index", 0)
            to_account_index: int = kwargs.get("to_account_index", 2)
            from_address_index: int = kwargs.get("from_address_index", 0)
            to_address_index: int = kwargs.get("to_address_index", 2)
            derivation: Union[
                IDerivation, BIP44Derivation, BIP49Derivation, BIP84Derivation, BIP86Derivation, CIP1852Derivation
            ] = self._derivation

            derivations: List[dict] = []
            for account_index in range(from_account_index, to_account_index):
                for address_index in range(from_address_index, to_address_index):
                    derivation.from_account(account=account_index)
                    derivation.from_address(address=address_index)
                    self.update_derivation(derivation=derivation)
                    derivations.append(get_derivation())
        elif self._derivation.name() == "Electrum":
            from_change_index: int = kwargs.get("from_change_index", 0)
            to_change_index: int = kwargs.get("to_change_index", 2)
            from_address_index: int = kwargs.get("from_address_index", 0)
            to_address_index: int = kwargs.get("to_address_index", 2)
            derivation: Union[
                IDerivation, ElectrumDerivation
            ] = self._derivation

            derivations: List[dict] = []
            for change_index in range(from_change_index, to_change_index):
                for address_index in range(from_address_index, to_address_index):
                    derivation.from_change(change=change_index)
                    derivation.from_address(address=address_index)
                    self.update_derivation(derivation=derivation)
                    derivations.append(get_derivation())
        else:
            from_index: int = kwargs.get("from_index", 0)
            to_index: int = kwargs.get("to_index", 5)
            indexes: List[int] = self.indexes()

            for index in range(from_index, to_index):
                custom_derivation: CustomDerivation = CustomDerivation(indexes=indexes)
                custom_derivation.from_index(index=index)
                self.update_derivation(derivation=custom_derivation)
                derivations.append(get_derivation())

        dumps.setdefault("derivations", derivations)
        return dumps
