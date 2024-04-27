#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Optional, Union, Any, Type, Tuple, List
)

from .libs.base58 import check_decode
from .entropies import (
    IEntropy, ENTROPIES
)
from .mnemonics import (
    IMnemonic, ElectrumV2Mnemonic, MoneroMnemonic, ELECTRUM_V2_MNEMONIC_TYPES, MNEMONICS
)
from .seeds import (
    ISeed, BIP39Seed, CardanoSeed, ElectrumV2Seed, SEEDS
)
from .hds import (
    IHD, HDS
)
from .ecc import (
    IPrivateKey, IPublicKey
)
from .const import (
    PUBLIC_KEY_TYPES, ELECTRUM_V2_MODES
)
from .cryptocurrencies.icryptocurrency import (
    ICryptocurrency, INetwork
)
from .keys import deserialize
from .exceptions import (
    Error, NetworkError, AddressError
)
from .utils import (
    get_bytes, exclude_keys
)
from .derivations import (
    IDerivation, DERIVATIONS
)
from .addresses import (
    IAddress, ADDRESSES
)


class HDWallet:

    _cryptocurrency: ICryptocurrency
    _network: INetwork
    _address: Type[IAddress]
    _address_type: Optional[str] = None

    _entropy: Optional[IEntropy] = None
    _language: Optional[str] = None
    _passphrase: Optional[str] = None
    _mnemonic: Optional[IMnemonic] = None
    _seed: Optional[ISeed] = None
    _derivation: Optional[IDerivation] = None

    _semantic: Optional[str] = None

    # Electrum-V2
    _mode: Optional[str] = None  # "standard" or "segwit"
    _mnemonic_type: Optional[str] = None  # "standard" or "segwit"

    _public_key_type: Optional[str] = None  # "uncompressed" or "compressed"
    _cardano_type: Optional[str] = None
    _use_default_path: bool = True
    # Monero entropy
    _checksum: bool = True
    _kwargs: Any

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
            raise Error(
                "Invalid cryptocurrency sub-class", expected=Type[ICryptocurrency], got=type(cryptocurrency)
            )
        self._cryptocurrency = cryptocurrency()

        if hd is None:  # Use default hd
            hd = HDS[self._cryptocurrency.DEFAULT_HD]
        elif hd is not None and not issubclass(hd, IHD):
            raise Error(
                "Invalid Hierarchical Deterministic (HD) sub-class", expected=Type[IHD], got=type(hd)
            )
        if hd.name() in [
            "BIP32", "BIP44", "BIP49", "BIP84", "BIP86", "BIP141", "Electrum-V1"
        ]:
            if not kwargs.get("public_key_type") and hd.name() == "Electrum-V1":
                self._public_key_type = kwargs.get("public_key_type", PUBLIC_KEY_TYPES.UNCOMPRESSED)
            elif not kwargs.get("public_key_type") and hd.name() != "Electrum-V1":
                self._public_key_type = kwargs.get("public_key_type", PUBLIC_KEY_TYPES.COMPRESSED)
            elif kwargs.get("public_key_type") in PUBLIC_KEY_TYPES.get_types():
                self._public_key_type = kwargs.get("public_key_type")
            else:
                raise Error(
                    f"Invalid {hd.name()} public key type",
                    expected=PUBLIC_KEY_TYPES.get_types(),
                    got=kwargs.get("public_key_type")
                )
        elif hd.name() == "Cardano":
            from .cryptocurrencies import Cardano
            if not kwargs.get("cardano_type"):
                self._cardano_type = kwargs.get("cardano_type", Cardano.TYPES.SHELLEY_ICARUS)
            elif Cardano.TYPES.is_cardano_type(kwargs.get("cardano_type")):
                self._cardano_type = kwargs.get("cardano_type")
            else:
                raise Error(
                    "Invalid Cardano type", expected=Cardano.TYPES.get_cardano_types(), got=kwargs.get("cardano_type")
                )
        elif hd.name() == "Electrum-V2":
            if not kwargs.get("mode"):
                self._mode = kwargs.get("mode", ELECTRUM_V2_MODES.STANDARD)  # Default
            elif kwargs.get("mode") in ELECTRUM_V2_MODES.get_modes():
                self._mode = kwargs.get("mode")
            else:
                raise Error(
                    f"Invalid {hd.name()} mode", expected=ELECTRUM_V2_MODES.get_modes(), got=kwargs.get("mode")
                )
            if not kwargs.get("mnemonic_type"):
                self._mnemonic_type = kwargs.get("mnemonic_type", ELECTRUM_V2_MNEMONIC_TYPES.STANDARD)  # Default
            elif kwargs.get("mnemonic_type") in ElectrumV2Mnemonic.mnemonic_types.keys():
                self._mnemonic_type = kwargs.get("mnemonic_type")
            else:
                raise Error(
                    f"Invalid {hd.name()} mnemonic type",
                    expected=ElectrumV2Mnemonic.mnemonic_types.keys(),
                    got=kwargs.get("mnemonic_type")
                )
            self._public_key_type = kwargs.get(
                "public_key_type", PUBLIC_KEY_TYPES.UNCOMPRESSED
            )
        elif hd.name() == "Monero":
            if not kwargs.get("checksum"):
                self._checksum = kwargs.get("checksum", False)  # Default
            elif isinstance(kwargs.get("checksum"), bool):
                self._checksum = kwargs.get("checksum")
            else:
                raise Error(
                    f"Invalid {hd.name()} checksum", expected=bool, got=type(kwargs.get("checksum"))
                )

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
        self._address = ADDRESSES.address(name=address)
        self._address_type = kwargs.get(
            "address_type", self._cryptocurrency.DEFAULT_ADDRESS_TYPE
        )

        if hd.name() not in cryptocurrency.HDS.get_hds():
            raise Error(
                f"{hd.name()} HD not implemented on {cryptocurrency.NAME} cryptocurrency"
            )

        self._semantic = kwargs.get(
            "semantic", "P2WPKH"
        )
        self._language = kwargs.get("language", "english")
        self._passphrase = kwargs.get("passphrase", None)
        self._use_default_path = kwargs.get("use_default_path", False)
        # self._cryptocurrency.get_default_path(network=self._network.__name__.lower())
        self._kwargs = {
            "staking_public_key": kwargs.get("staking_public_key", None),
            "payment_id": kwargs.get("payment_id", None)
        }

        if hd.name() in [
            "BIP32", "BIP44", "BIP49", "BIP84", "BIP86", "BIP141"
        ]:
            self._hd = hd(
                ecc=cryptocurrency.ECC, public_key_type=self._public_key_type, semantic=self._semantic
            )
        elif hd.name() == "Cardano":
            self._hd = hd(cardano_type=self._cardano_type)
        elif hd.name() == "Electrum-V1":
            self._hd = hd(public_key_type=self._public_key_type)
        elif hd.name() == "Electrum-V2":
            self._hd = hd(mode=self._mode, public_key_type=self._public_key_type)
        elif hd.name() == "Monero":
            self._hd = hd(network=self._network.__name__.lower())

    def from_entropy(self, entropy: IEntropy) -> "HDWallet":

        if entropy.name() not in self._cryptocurrency.ENTROPIES.get_entropies():
            raise Error(f"Invalid entropy class for {self._cryptocurrency.NAME} cryptocurrency")
        self._entropy = entropy

        if self._entropy.name() == "Electrum-V2":
            mnemonic: str = ElectrumV2Mnemonic.from_entropy(
                entropy=self._entropy.entropy(), language=self._language, mnemonic_type=self._mnemonic_type
            )
        elif self._entropy.name() == "Monero":
            mnemonic: str = MoneroMnemonic.from_entropy(
                entropy=self._entropy.entropy(), language=self._language, checksum=self._checksum
            )
        else:
            mnemonic: str = MNEMONICS.mnemonic(
                name=self._entropy.name()
            ).from_entropy(
                entropy=self._entropy.entropy(), language=self._language
            )

        if self._entropy.name() == "Electrum-V2":
            return self.from_mnemonic(
                mnemonic=ElectrumV2Mnemonic(
                    mnemonic=mnemonic, mnemonic_type=self._mnemonic_type
                )
            )
        return self.from_mnemonic(
            mnemonic=MNEMONICS.mnemonic(
                name=self._entropy.name()
            ).__call__(
                mnemonic=mnemonic
            )
        )

    def from_mnemonic(self, mnemonic: IMnemonic) -> "HDWallet":

        if mnemonic.name() not in self._cryptocurrency.MNEMONICS.get_mnemonics():
            raise Error(f"Invalid mnemonic class for {self._cryptocurrency.NAME} cryptocurrency")
        self._mnemonic = mnemonic

        if self._mnemonic.name() == "Electrum-V2":
            self._entropy = ENTROPIES.entropy(
                name=self._mnemonic.name()
            ).__call__(
                entropy=self._mnemonic.decode(
                    mnemonic=self._mnemonic.mnemonic(),
                    mnemonic_type=self._mnemonic_type
                )
            )
        else:
            self._entropy = ENTROPIES.entropy(
                name=self._mnemonic.name()
            ).__call__(
                entropy=self._mnemonic.decode(
                    mnemonic=self._mnemonic.mnemonic()
                )
            )

        if mnemonic.name() == "BIP39" and self._hd.name() == "Cardano":
            seed: str = CardanoSeed.from_mnemonic(
                mnemonic=self._mnemonic.mnemonic(),
                passphrase=self.passphrase(),
                cardano_type=self._cardano_type
            )
        elif mnemonic.name() == BIP39Seed.name():
            seed: str = BIP39Seed.from_mnemonic(
                mnemonic=self._mnemonic.mnemonic(),
                passphrase=self.passphrase()
            )
        elif mnemonic.name() == ElectrumV2Seed.name():
            seed: str = ElectrumV2Seed.from_mnemonic(
                mnemonic=self._mnemonic.mnemonic(),
                passphrase=self.passphrase(),
                mnemonic_type=self._mnemonic_type
            )
        else:
            seed: str = SEEDS.seed(
                name=self._mnemonic.name()
            ).from_mnemonic(
                mnemonic=self._mnemonic.mnemonic()
            )
        return self.from_seed(
            seed=SEEDS.seed(
                name=(
                    "Cardano" if self._hd.name() == "Cardano" else self._mnemonic.name()
                )
            ).__call__(
                seed=seed
            )
        )

    def from_seed(self, seed: ISeed) -> "HDWallet":

        if seed.name() not in self._cryptocurrency.SEEDS.get_seeds():
            raise Error(f"Invalid seed class for {self._cryptocurrency.NAME} cryptocurrency")
        self._seed = seed

        self._hd.from_seed(
            seed=seed.seed(), passphrase=self.passphrase()
        )
        return self

    def from_xprivate_key(self, xprivate_key: str, encoded: bool = True, strict: bool = False) -> "HDWallet":

        if self._hd.name() in ["Electrum-V1", "Monero"]:
            raise Error(f"Conversion from xprivate key is not implemented for the {self._hd.name()} HD type")

        version, depth, parent_fingerprint, index, chain_code, key = deserialize(
            key=xprivate_key, encoded=encoded
        )

        if not self._network.XPRIVATE_KEY_VERSIONS.is_version(version=version) or \
                len(check_decode(xprivate_key) if encoded else xprivate_key) not in [78, 110]:
            raise Error(f"Invalid {self._cryptocurrency.NAME} extended(x) private key")

        self._hd.from_xprivate_key(
            xprivate_key=xprivate_key, encoded=encoded, strict=strict
        )
        return self

    def from_xpublic_key(self, xpublic_key: str, encoded: bool = True, strict: bool = False) -> "HDWallet":

        if self._hd.name() in ["Electrum-V1", "Monero"]:
            raise Error(
                f"Conversion from xpublic key is not implemented for the {self._hd.name()} HD type"
            )
        elif self._hd.name() == "Cardano" and self._cardano_type == "byron-legacy":
            raise Error(
                f"Conversion from xpublic key is not implemented for the {self._hd.name()} HD {self._cardano_type} type"
            )

        version, depth, parent_fingerprint, index, chain_code, key = deserialize(
            key=xpublic_key, encoded=encoded
        )

        if not self._network.XPUBLIC_KEY_VERSIONS.is_version(version=version) or \
                len(check_decode(xpublic_key) if encoded else xpublic_key) not in [78, 110]:
            raise Error(f"Invalid {self._cryptocurrency.NAME} extended(x) public key")

        self._hd.from_xpublic_key(
            xpublic_key=xpublic_key, encoded=encoded, strict=strict
        )
        return self

    def from_derivation(self, derivation: IDerivation) -> "HDWallet":
        self._hd.from_derivation(derivation=derivation)
        self._derivation = derivation
        return self

    def update_derivation(self, derivation: IDerivation) -> "HDWallet":
        self._hd.update_derivation(derivation=derivation)
        self._derivation = derivation
        return self

    def clean_derivation(self) -> "HDWallet":
        self._hd.clean_derivation()
        self._derivation.clean()
        return self

    def from_private_key(self, private_key: str) -> "HDWallet":
        self._hd.from_private_key(private_key=private_key)
        return self

    def from_wif(self, wif: str) -> "HDWallet":
        if self._hd.name() in ["Cardano", "Monero"]:
            raise Error(f"Wallet Important Format (WIF) is not supported by {self._hd.name()} HD wallet's")

        self._hd.from_wif(wif=wif)
        return self

    def from_public_key(self, public_key: str) -> "HDWallet":
        if self._hd.name() in ["Monero"]:
            raise Error(f"From public key is not implemented for the {self._hd.name()} HD type")
        self._hd.from_public_key(public_key=public_key)
        return self

    def from_spend_private_key(
        self, spend_private_key: Union[bytes, str, IPrivateKey]
    ) -> "HDWallet":
        if self._hd.name() != "Monero":
            raise Error("From spend private key only supported by Monero HD ")
        self._hd.from_spend_private_key(spend_private_key=spend_private_key)
        return self

    def from_watch_only(
        self,
        view_private_key: Union[bytes, str, IPrivateKey],
        spend_public_key: Union[bytes, str, IPublicKey]
    ) -> "HDWallet":
        if self._hd.name() != "Monero":
            raise Error("From spend watch only supported by Monero HD wallet")
        self._hd.from_watch_only(
            view_private_key=view_private_key, spend_public_key=spend_public_key
        )
        return self

    def cryptocurrency(self) -> str:
        return self._cryptocurrency.NAME

    def symbol(self) -> str:
        return self._cryptocurrency.SYMBOL

    def coin_type(self) -> int:
        return self._cryptocurrency.COIN_TYPE

    def network(self) -> str:
        return self._network.__name__.lower()

    def entropy(self) -> Optional[str]:
        return self._entropy.entropy() if self._entropy else None

    def strength(self) -> Optional[str]:
        return self._entropy.strength() if self._entropy else None

    def mnemonic(self) -> Optional[str]:
        return self._mnemonic.mnemonic() if self._mnemonic else None

    def mnemonic_type(self) -> Optional[str]:
        return self._mnemonic_type if self._mnemonic_type else None

    def language(self) -> Optional[str]:
        return self._mnemonic.language() if self._mnemonic else None

    def words(self) -> Optional[int]:
        return self._mnemonic.words() if self._mnemonic else None

    def passphrase(self) -> Optional[str]:
        return self._passphrase if self._passphrase else None

    def seed(self) -> Optional[str]:
        return self._hd.seed()

    def ecc(self) -> str:
        return self._cryptocurrency.ECC.NAME

    def hd(self) -> str:
        return self._hd.name()

    def semantic(self) -> Optional[str]:
        if self._hd.name() == "BIP141":
            return self._hd.semantic()
        return None

    def cardano_type(self) -> Optional[str]:
        if self._hd.name() == "Cardano":
            return self._cardano_type
        return None

    def mode(self) -> str:

        if self._hd.name() not in ["Electrum-V2"]:
            raise Error(f"Get mode is only for {self._hd.name()} HD type")

        return self._hd.mode()

    def path_key(self) -> Optional[str]:
        return self._hd.path_key()

    def root_xprivate_key(self, semantic: str = "P2PKH", encoded: bool = True) -> Optional[str]:

        if self._hd.name() in ["Electrum-V1", "Monero"]:
            return None

        return self._hd.root_xprivate_key(
            version=self._network.XPRIVATE_KEY_VERSIONS.get_version(semantic), encoded=encoded
        )

    def root_xpublic_key(self, semantic: str = "P2PKH", encoded: bool = True) -> Optional[str]:

        if self._hd.name() in ["Electrum-V1", "Monero"]:
            return None

        return self._hd.root_xpublic_key(
            version=self._network.XPUBLIC_KEY_VERSIONS.get_version(semantic), encoded=encoded
        )

    def master_xprivate_key(self, semantic: str = "P2PKH", encoded: bool = True) -> Optional[str]:
        return self.root_xprivate_key(semantic=semantic, encoded=encoded)

    def master_xpublic_key(self, semantic: str = "P2PKH", encoded: bool = True) -> Optional[str]:
        return self.root_xpublic_key(semantic=semantic, encoded=encoded)

    def root_private_key(self) -> Optional[str]:
        if self._hd.name() in ["Electrum-V1", "Electrum-V2"]:
            return self._hd.master_private_key()
        return self._hd.root_private_key()

    def root_wif(self, wif_type: Optional[str] = None) -> Optional[str]:
        if self._hd.name() not in ["Cardano"]:
            if self._hd.name() in ["Electrum-V1", "Electrum-V2"]:
                return self._hd.master_wif(wif_type=wif_type)
            return self._hd.root_wif(wif_type=wif_type)
        return None

    def root_chain_code(self) -> Optional[str]:
        return self._hd.root_chain_code()

    def root_public_key(self, public_key_type: Optional[str] = None) -> Optional[str]:
        if self._hd.name() in ["Electrum-V1", "Electrum-V2"]:
            return self._hd.master_public_key(public_key_type=public_key_type)
        return self._hd.root_public_key(public_key_type=public_key_type)

    def master_private_key(self) -> Optional[str]:
        if self._hd.name() in ["Electrum-V1", "Electrum-V2"]:
            return self._hd.master_private_key()
        return self._hd.root_private_key()

    def master_wif(self, wif_type: Optional[str] = None) -> Optional[str]:
        if self._hd.name() not in ["Cardano"]:
            if self._hd.name() in ["Electrum-V1", "Electrum-V2"]:
                return self._hd.master_wif(wif_type=wif_type)
            return self._hd.root_wif(wif_type=wif_type)
        return None

    def master_chain_code(self) -> Optional[str]:
        return self._hd.root_chain_code()

    def master_public_key(self, public_key_type: Optional[str] = None) -> Optional[str]:
        if self._hd.name() in ["Electrum-V1", "Electrum-V2"]:
            return self._hd.master_public_key(public_key_type=public_key_type)
        return self._hd.root_public_key(public_key_type=public_key_type)

    def xprivate_key(self, semantic: str = "P2PKH", encoded: bool = True) -> Optional[str]:

        if self._hd.name() in ["Electrum-V1", "Monero"]:
            return None

        return self._hd.xprivate_key(
            version=self._network.XPRIVATE_KEY_VERSIONS.get_version(semantic), encoded=encoded
        )

    def xpublic_key(self, semantic: str = "P2PKH", encoded: bool = True) -> Optional[str]:

        if self._hd.name() in ["Electrum-V1", "Monero"]:
            return None

        return self._hd.xpublic_key(
            version=self._network.XPUBLIC_KEY_VERSIONS.get_version(semantic), encoded=encoded
        )

    def private_key(self) -> Optional[str]:
        return self._hd.private_key()

    def spend_private_key(self) -> str:
        if self._hd.name() != "Monero":
            raise Error("Spend private key only supported by Monero HD wallet")
        return self._hd.spend_private_key()

    def view_private_key(self) -> str:
        if self._hd.name() != "Monero":
            raise Error("View private key only supported by Monero HD wallet")
        return self._hd.view_private_key()

    def wif(self, wif_type: Optional[str] = None) -> Optional[str]:
        if self._hd.name() not in ["Cardano"]:
            return self._hd.wif(wif_type=wif_type)
        return None

    def wif_type(self) -> Optional[str]:
        return self._hd.wif_type() if self.wif() else None

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
            raise Error("Spend public key only supported by Monero HD wallet")
        return self._hd.spend_public_key()

    def view_public_key(self) -> str:
        if self._hd.name() != "Monero":
            raise Error("view public key only supported by Monero HD wallet")
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

    def strict(self) -> Optional[bool]:
        if self._hd.name() not in ["Electrum-V1", "Monero"]:
            return self._hd.strict()
        return None

    def primary_address(self) -> Optional[str]:
        if self._hd.name() == "Monero":
            return self._hd.primary_address()

    def integrated_address(self, payment_id: Union[bytes, str]) -> Optional[str]:
        if self._hd.name() == "Monero":
            return self._hd.integrated_address(payment_id=payment_id)

    def sub_address(self, minor: Optional[int] = None, major: Optional[int] = None) -> Optional[str]:
        if self._hd.name() == "Monero":
            return self._hd.sub_address(
                minor=minor, major=major
            )

    def address(self, address: Optional[Union[str, Type[IAddress]]] = None, **kwargs) -> str:

        if address is None:
            address = self._address.name()
        elif not isinstance(address, str) and issubclass(address, IAddress):
            address = address.name()
        if address not in self._cryptocurrency.ADDRESSES.get_addresses():
            raise AddressError(
                f"Wrong {self._cryptocurrency.NAME} address",
                expected=self._cryptocurrency.ADDRESSES.get_addresses(),
                got=address
            )

        if self._network.WITNESS_VERSIONS:
            kwargs.setdefault(
                "witness_version", self._network.WITNESS_VERSIONS.get_witness_version(address)
            )

        if self._hd.name() == "Cardano":
            return self._hd.address(
                network=self._network.__name__.lower(), **kwargs
            )
        elif self._hd.name() in "Electrum-V1":
            return self._hd.address(
                public_key_address_prefix=self._network.PUBLIC_KEY_ADDRESS_PREFIX
            )
        elif self._hd.name() in "Electrum-V2":
            return self._hd.address(
                public_key_address_prefix=self._network.PUBLIC_KEY_ADDRESS_PREFIX,
                hrp=self._network.HRP,
                witness_version=self._network.WITNESS_VERSIONS.get_witness_version("P2WPKH")
            )
        elif self._hd.name() == "Monero":
            if kwargs.get("version_type") == "standard":
                return self.primary_address()
            elif kwargs.get("version_type") == "integrated":
                return self.integrated_address(
                    payment_id=get_bytes(kwargs.get("payment_id"))
                )
            elif kwargs.get("version_type") == "sub-address":
                return self.sub_address(
                    minor=kwargs.get("minor", None), major=kwargs.get("major", None)
                )
        else:
            return ADDRESSES.address(name=address).encode(
                public_key=self.public_key(),
                public_key_address_prefix=self._network.PUBLIC_KEY_ADDRESS_PREFIX,
                script_address_prefix=self._network.SCRIPT_ADDRESS_PREFIX,
                network_type=self._network.__name__.lower(),
                public_key_type=self.public_key_type(),
                hrp=self._network.HRP,
                address_type=kwargs.get(
                    "address_type", self._address_type
                ),
                **kwargs
            )

    def dump(self, exclude: Optional[set] = None) -> dict:

        if exclude is None:
            exclude = { }

        _derivation: dict = { }

        if self._derivation:
            if self._derivation.name() in [
                "BIP44", "BIP49", "BIP84", "BIP86"
            ]:
                _at: dict = dict(
                    path=self._derivation.path(),
                    indexes=self._derivation.indexes(),
                    depth=self.depth(),
                    purpose=self._derivation.purpose(),
                    coin_type=self._derivation.coin_type(),
                    account=self._derivation.account(),
                    change=self._derivation.change(),
                    address=self._derivation.address()
                )
            elif self._derivation.name() == "CIP1852":
                _at: dict = dict(
                    path=self._derivation.path(),
                    indexes=self._derivation.indexes(),
                    depth=self.depth(),
                    purpose=self._derivation.purpose(),
                    coin_type=self._derivation.coin_type(),
                    account=self._derivation.account(),
                    role=self._derivation.role(),
                    address=self._derivation.address()
                )
            elif self._derivation.name() == "Electrum":
                _at: dict = dict(
                    change=self._derivation.change(),
                    address=self._derivation.address()
                )
            elif self._derivation.name() == "Monero":
                _at: dict = dict(
                    minor=self._derivation.minor(),
                    major=self._derivation.major()
                )
            else:
                _at: dict = dict(
                    path=self._derivation.path(),
                    indexes=self._derivation.indexes(),
                    depth=self.depth(),
                    index=self.index()
                )
            _derivation.update(
                at=_at
            )

        if self._hd.name() in [
            "BIP32", "BIP44", "BIP49", "BIP84", "BIP86", "BIP141", "Cardano"
        ]:
            _derivation.update(
                xprivate_key=self.xprivate_key(),
                xpublic_key=self.xpublic_key(),
                private_key=self.private_key(),
                wif=self.wif(),
                chain_code=self.chain_code(),
                public_key=self.public_key(),
                uncompressed=self.uncompressed(),
                compressed=self.compressed(),
                hash=self.hash(),
                fingerprint=self.fingerprint(),
                parent_fingerprint=self.parent_fingerprint()
            )
            if self._hd.name() == "Cardano":
                del _derivation["wif"]
                del _derivation["uncompressed"]
                del _derivation["compressed"]

            if (
                self._cryptocurrency.ADDRESSES.length() > 1 or
                self._cryptocurrency.NAME in ["Tezos"]
            ):
                addresses: dict = { }
                if self._cryptocurrency.NAME == "Avalanche":
                    addresses[self._cryptocurrency.ADDRESS_TYPES.C_CHAIN] = self.address(address="Ethereum")
                    addresses[self._cryptocurrency.ADDRESS_TYPES.P_CHAIN] = self.address(
                        address="Avalanche", address_type=self._cryptocurrency.ADDRESS_TYPES.P_CHAIN
                    )
                    addresses[self._cryptocurrency.ADDRESS_TYPES.X_CHAIN] = self.address(
                        address="Avalanche", address_type=self._cryptocurrency.ADDRESS_TYPES.X_CHAIN
                    )
                elif self._cryptocurrency.NAME == "Binance":
                    addresses[self._cryptocurrency.ADDRESS_TYPES.CHAIN] = self.address(address="Cosmos")
                    addresses[self._cryptocurrency.ADDRESS_TYPES.SMART_CHAIN] = self.address(address="Ethereum")
                elif self._cryptocurrency.NAME in ["Bitcoin-Cash", "Bitcoin-Cash-SLP", "eCash"]:
                    for address_type in self._cryptocurrency.ADDRESS_TYPES.get_address_types():
                        for address in self._cryptocurrency.ADDRESSES.get_addresses():
                            addresses[f"{address_type}-{address.lower()}"] = ADDRESSES.address(name=address).encode(
                                public_key=self.public_key(),
                                public_key_address_prefix=getattr(
                                    self._network, f"{address_type.upper()}_PUBLIC_KEY_ADDRESS_PREFIX"
                                ),
                                script_address_prefix=getattr(
                                    self._network, f"{address_type.upper()}_SCRIPT_ADDRESS_PREFIX"
                                ),
                                public_key_type=self.public_key_type(),
                                hrp=self._network.HRP
                            )
                elif self._cryptocurrency.NAME == "Tezos":
                    addresses[self._cryptocurrency.ADDRESS_PREFIXES.TZ1] = self.address(
                        address_prefix=self._cryptocurrency.ADDRESS_PREFIXES.TZ1
                    )
                    addresses[self._cryptocurrency.ADDRESS_PREFIXES.TZ2] = self.address(
                        address_prefix=self._cryptocurrency.ADDRESS_PREFIXES.TZ2
                    )
                    addresses[self._cryptocurrency.ADDRESS_PREFIXES.TZ3] = self.address(
                        address_prefix=self._cryptocurrency.ADDRESS_PREFIXES.TZ3
                    )
                elif self._hd.name() == "BIP44":
                    _derivation["address"] = self.address(address="P2PKH")
                elif self._hd.name() == "BIP49":
                    _derivation["address"] = self.address(address="P2WPKH-In-P2SH")
                elif self._hd.name() == "BIP84":
                    _derivation["address"] = self.address(address="P2WPKH")
                elif self._hd.name() == "BIP86":
                    _derivation["address"] = self.address(address="P2TR")
                else:
                    for address in self._cryptocurrency.ADDRESSES.get_addresses():
                        if self._hd.name() == "BIP141" and address in [
                            "P2PKH", "P2SH", "P2TR"
                        ]:
                            continue
                        addresses[address.lower().replace("-", "_")] = self.address(address=address)
                if addresses:
                    _derivation["addresses"] = addresses
            else:
                if (
                    self._cryptocurrency.NAME == "Cardano" and
                    self._cardano_type in ["shelley-icarus", "shelley-ledger"]
                ):
                    _derivation["address"] = self.address(
                        address_type=self._address_type, staking_public_key=self._kwargs.get("staking_public_key")
                    )
                else:
                    _derivation["address"] = self.address()

        elif self._hd.name() in ["Electrum-V1", "Electrum-V2"]:
            _derivation.update(
                private_key=self.private_key(),
                wif=self.wif(),
                public_key=self.public_key(),
                uncompressed=self.uncompressed(),
                compressed=self.compressed(),
                address=self.address()
            )
        elif self._hd.name() == "Monero":
            _derivation.update(
                sub_address=self.sub_address()
            )

        if "at" in exclude:
            del _derivation["at"]

        if "root" in exclude:
            return exclude_keys(_derivation, exclude)

        _root: dict = dict(
            cryptocurrency=self.cryptocurrency(),
            symbol=self.symbol(),
            network=self.network(),
            coin_type=self.coin_type(),
            entropy=self.entropy(),
            strength=self.strength(),
            mnemonic=self.mnemonic(),
            passphrase=self.passphrase(),
            language=self.language(),
            seed=self.seed(),
            ecc=self.ecc(),
            hd=self.hd()
        )
        if self._hd.name() in [
            "BIP32", "BIP44", "BIP49", "BIP84", "BIP86", "BIP141", "Cardano"
        ]:
            if self._hd.name() == "BIP141":
                _root.update(
                    semantic=self.semantic()
                )
            if self._hd.name() == "Cardano":
                _root.update(
                    cardano_type=self.cardano_type()
                )
            _root.update(
                root_xprivate_key=self.root_xprivate_key(),
                root_xpublic_key=self.root_xpublic_key(),
                root_private_key=self.root_private_key(),
                root_wif=self.root_wif(),
                root_chain_code=self.root_chain_code(),
                root_public_key=self.root_public_key(),
                path_key=self.path_key(),
                strict=self.strict(),
                public_key_type=self.public_key_type(),
                wif_type=self.wif_type()
            )
            if self._hd.name() == "Cardano":
                del _root["root_wif"]
                del _root["wif_type"]
                if self._cardano_type != "byron-legacy":
                    del _root["path_key"]
            else:
                del _root["path_key"]

        elif self._hd.name() in ["Electrum-V1", "Electrum-V2"]:
            if self._hd.name() == "Electrum-V2":
                _root.update(
                    mode=self.mode(),
                    mnemonic_type=self.mnemonic_type()
                )
            _root.update(
                master_private_key=self.master_private_key(),
                master_wif=self.master_wif(),
                master_public_key=self.master_public_key(),
                public_key_type=self.public_key_type(),
                wif_type=self.wif_type()
            )
        elif self._hd.name() == "Monero":
            _root.update(
                private_key=self.private_key(),
                spend_private_key=self.spend_private_key(),
                view_private_key=self.view_private_key(),
                spend_public_key=self.spend_public_key(),
                view_public_key=self.view_public_key(),
                primary_address=self.primary_address(),
            )
            if self._kwargs.get("payment_id"):
                _root.update(
                    integrated_address=self.integrated_address(
                        payment_id=self._kwargs.get("payment_id")
                    )
                )

        if "derivation" not in exclude:
            _root["derivation"] = _derivation

        return exclude_keys(_root, exclude)

    def dumps(self, exclude: Optional[set] = None) -> Optional[Union[dict, List[dict]]]:

        if exclude is None:
            exclude = { }

        _derivations: List[dict] = []

        def drive(*args) -> List[str]:
            def drive_helper(derivations, current_derivation: List[Tuple[int, bool]] = []) -> List[str]:
                if not derivations:

                    if self._derivation.name() in [
                        "BIP44", "BIP49", "BIP84", "BIP86"
                    ]:
                        _derivation: IDerivation = DERIVATIONS.derivation(
                            name=self._derivation.name()
                        ).__call__(
                            coin_type=current_derivation[1][0],
                            account=current_derivation[2][0],
                            change=current_derivation[3],
                            address=current_derivation[4][0]
                        )
                    elif self._derivation.name() == "CIP1852":
                        _derivation: IDerivation = DERIVATIONS.derivation(
                            name=self._derivation.name()
                        ).__call__(
                            coin_type=current_derivation[1][0],
                            account=current_derivation[2][0],
                            role=current_derivation[3],
                            address=current_derivation[4][0]
                        )
                    elif self._derivation.name() == "Electrum":
                        _derivation: IDerivation = DERIVATIONS.derivation(
                            name=self._derivation.name()
                        ).__call__(
                            change=current_derivation[0][0],
                            address=current_derivation[1][0]
                        )
                    elif self._derivation.name() == "Monero":
                        _derivation: IDerivation = DERIVATIONS.derivation(
                            name=self._derivation.name()
                        ).__call__(
                            minor=current_derivation[0][0],
                            major=current_derivation[1][0]
                        )
                    else:
                        _derivation: IDerivation = DERIVATIONS.derivation(
                            name=self._derivation.name()
                        ).__call__(
                            path="m/" + "/".join(
                                [str(item[0]) + "'" if item[1] else str(item[0]) for item in current_derivation]
                            )
                        )
                    self.update_derivation(derivation=_derivation)
                    _derivations.append(self.dump(exclude={"root", *exclude}))
                    return [_derivation.path()]

                path: List[str] = []
                if len(derivations[0]) == 3:
                    for value in range(derivations[0][0], derivations[0][1] + 1):
                        path += drive_helper(
                            derivations[1:], current_derivation + [(value, derivations[0][2])]
                        )
                else:
                    path += drive_helper(
                        derivations[1:], current_derivation + [derivations[0]]
                    )
                return path
            return drive_helper(args)

        if self._derivation is None:
            return None

        drive(*self._derivation.derivations())

        if "root" in exclude:
            return _derivations

        _root: dict = self.dump(exclude={"derivation"})

        if "derivations" not in exclude:
            _root["derivations"] = _derivations

        return exclude_keys(_root, exclude)
