#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Type, List, Tuple
)

import json
import click
import sys
import csv

from ..entropies import ENTROPIES
from ..mnemonics import MNEMONICS
from ..seeds import SEEDS
from ..hds import (
    BIP32HD, BIP44HD, BIP49HD, BIP84HD, BIP86HD, BIP141HD, CardanoHD, ElectrumV1HD, ElectrumV2HD, MoneroHD, HDS
)
from ..derivations import (
    IDerivation,
    BIP44Derivation,
    BIP49Derivation,
    BIP84Derivation,
    BIP86Derivation,
    CIP1852Derivation,
    CustomDerivation,
    ElectrumDerivation,
    MoneroDerivation,
    DERIVATIONS,
    CHANGES,
    ROLES
)
from ..cryptocurrencies import (
    ICryptocurrency, get_cryptocurrency
)
from ..hdwallet import HDWallet


def dumps(**kwargs) -> None:
    try:
        cryptocurrency: Type[ICryptocurrency] = get_cryptocurrency(
            symbol=kwargs.get("symbol")
        )
        if kwargs.get("hd") not in HDS.keys():
            click.echo(click.style(
                f"Wrong HD name, (expected={list(HDS.keys())}, got='{kwargs.get('hd')}')"
            ), err=True)
            sys.exit()
        if kwargs.get("derivation") not in DERIVATIONS.keys():
            click.echo(click.style(
                f"Wrong from derivation name, (expected={list(DERIVATIONS.keys())}, got='{kwargs.get('derivation')}')"
            ), err=True)
            sys.exit()
        if not cryptocurrency.NETWORKS.is_network(network=kwargs.get("network")):
            click.echo(click.style(
                f"Invalid {cryptocurrency.NAME} cryptocurrency network, "
                f"(expected={cryptocurrency.NETWORKS.get_networks()}, got='{kwargs.get('network')}')"
            ), err=True)
            sys.exit()

        hdwallet: HDWallet = HDWallet(
            cryptocurrency=cryptocurrency,
            hd=HDS[kwargs.get("hd")],
            network=kwargs.get("network"),
            public_key_type=kwargs.get("public_key_type"),
            passphrase=kwargs.get("passphrase"),
            cardano_type=kwargs.get("cardano_type"),
            address_type=kwargs.get("address_type"),
            staking_public_key=kwargs.get("staking_public_key"),
            mode=kwargs.get("mode"),
            mnemonic_type=kwargs.get("mnemonic_type"),
            checksum=kwargs.get("checksum"),
            semantic=kwargs.get("semantic")
        )

        if kwargs.get("entropy"):
            if kwargs.get("entropy_name") not in ENTROPIES.keys():
                click.echo(click.style(
                    f"Wrong entropy name, (expected={list(ENTROPIES.keys())}, got='{kwargs.get('entropy_name')}')"
                ), err=True)
                sys.exit()
            hdwallet.from_entropy(
                entropy=ENTROPIES[kwargs.get("entropy_name")](
                    entropy=kwargs.get("entropy")
                )
            )
        elif kwargs.get("mnemonic"):
            if kwargs.get("mnemonic_name") not in MNEMONICS.keys():
                click.echo(click.style(
                    f"Wrong mnemonic name, (expected={list(MNEMONICS.keys())}, got='{kwargs.get('mnemonic_name')}')"
                ), err=True)
                sys.exit()
            hdwallet.from_mnemonic(
                mnemonic=MNEMONICS[kwargs.get("mnemonic_name")](
                    mnemonic=kwargs.get("mnemonic")
                )
            )
        elif kwargs.get("seed"):
            if kwargs.get("seed_name") not in SEEDS.keys():
                click.echo(click.style(
                    f"Wrong seed name, (expected={list(SEEDS.keys())}, got='{kwargs.get('seed_name')}')"
                ), err=True)
                sys.exit()
            hdwallet.from_seed(
                seed=SEEDS[kwargs.get("seed_name")](
                    seed=kwargs.get("seed")
                )
            )
        elif kwargs.get("xprivate_key"):
            hdwallet.from_xprivate_key(
                xprivate_key=kwargs.get("xprivate_key"),
                encoded=kwargs.get("encoded"),
                strict=kwargs.get("strict")
            )
        elif kwargs.get("xpublic_key"):
            hdwallet.from_xpublic_key(
                xpublic_key=kwargs.get("xpublic_key"),
                encoded=kwargs.get("encoded"),
                strict=kwargs.get("strict")
            )
        elif kwargs.get("private_key"):
            hdwallet.from_private_key(
                private_key=kwargs.get("private_key")
            )
        elif kwargs.get("wif"):
            hdwallet.from_wif(
                wif=kwargs.get("wif")
            )
        elif kwargs.get("public_key"):
            hdwallet.from_public_key(
                public_key=kwargs.get("public_key")
            )
        elif kwargs.get("spend_private_key"):
            hdwallet.from_spend_private_key(
                spend_private_key=kwargs.get("spend_private_key")
            )
        elif kwargs.get("view_private_key") and kwargs.get("spend_public_key"):
            hdwallet.from_watch_only(
                view_private_key=kwargs.get("view_private_key"),
                spend_public_key=kwargs.get("spend_public_key")
            )

        if (
            kwargs.get("entropy") or
            kwargs.get("mnemonic") or
            kwargs.get("seed") or
            kwargs.get("xprivate_key") or
            kwargs.get("xpublic_key") or
            (kwargs.get("private_key") and kwargs.get("hd") in ["Electrum-V1", "Monero"]) or
            (kwargs.get("wif") and kwargs.get("hd") == "Electrum-V1") or
            kwargs.get("spend_private_key") or
            (kwargs.get("view_private_key") and kwargs.get("spend_public_key"))
        ):

            if kwargs.get("derivation") in [
                BIP44Derivation.name(), BIP49Derivation.name(), BIP84Derivation.name(), BIP86Derivation.name()
            ]:
                if kwargs.get("change") in ["0", "external-chain"]:
                    change: str = CHANGES.EXTERNAL_CHAIN
                elif kwargs.get("change") in ["1", "internal-chain"]:
                    change: str = CHANGES.INTERNAL_CHAIN
                else:
                    click.echo(click.style(
                        f"Wrong {kwargs.get('derivation')} change index, "
                        f"(expected= 0 | external-chain | 1 | internal-chain, "
                        f"got='{kwargs.get('change')}')"
                    ), err=True)
                    sys.exit()

                hdwallet.from_derivation(
                    derivation=DERIVATIONS[kwargs.get("derivation")](
                        coin_type=cryptocurrency.COIN_TYPE,
                        account=tuple([int(account) for account in kwargs.get("account").split("-")]),
                        change=change,
                        address=tuple([int(address) for address in kwargs.get("address").split("-")])
                    )
                )
            elif kwargs.get("derivation") == CIP1852Derivation.name():

                if kwargs.get("role") in ["0", "external-chain"]:
                    role: str = ROLES.EXTERNAL_CHAIN
                elif kwargs.get("role") in ["1", "internal-chain"]:
                    role: str = ROLES.INTERNAL_CHAIN
                elif kwargs.get("role") in ["2", "staking-chain"]:
                    role: str = ROLES.STAKING_KEY
                else:
                    click.echo(click.style(
                        f"Wrong {kwargs.get('derivation')} role index, "
                        f"(expected= 0 | external-chain | 1 | internal-chain | 2 | staking-chain, "
                        f"got='{kwargs.get('role')}')"
                    ), err=True)
                    sys.exit()

                hdwallet.from_derivation(
                    derivation=DERIVATIONS[kwargs.get("derivation")](
                        coin_type=cryptocurrency.COIN_TYPE,
                        account=tuple([int(account) for account in kwargs.get("account").split("-")]),
                        role=role,
                        address=tuple([int(address) for address in kwargs.get("address").split("-")])
                    )
                )
            elif kwargs.get("derivation") == CustomDerivation.name():
                hdwallet.from_derivation(
                    derivation=DERIVATIONS[kwargs.get("derivation")](
                        path=kwargs.get("path", "m/"),
                        indexes=kwargs.get("indexes", [])
                    )
                )
            elif kwargs.get("derivation") == ElectrumDerivation.name():
                hdwallet.from_derivation(
                    derivation=DERIVATIONS[kwargs.get("derivation")](
                        change=tuple([int(change) for change in kwargs.get("change").split("-")]),
                        address=tuple([int(address) for address in kwargs.get("address").split("-")])
                    )
                )
            elif kwargs.get("derivation") == MoneroDerivation.name():
                hdwallet.from_derivation(
                    derivation=DERIVATIONS[kwargs.get("derivation")](
                        minor=tuple([int(minor) for minor in kwargs.get("minor").split("-")]),
                        major=tuple([int(major) for major in kwargs.get("major").split("-")])
                    )
                )

        if kwargs.get("format") == "csv":

            hd_name: str = hdwallet._hd.name()
            if kwargs.get("show"):
                _show: str = kwargs.get("show")
            elif hd_name == BIP32HD.name():
                _show: str = "at:path,addresses:p2pkh,public_key,wif"
            elif hd_name in [
                BIP44HD.name(), BIP49HD.name(), BIP84HD.name(), BIP86HD.name()
            ]:
                _show: str = "at:path,address,public_key,wif"
            elif hd_name == BIP141HD.name():
                _show: str = f"at:path,addresses:p2wpkh,public_key,wif"
            elif hd_name == CardanoHD.name():
                _show: str = "at:path,address,public_key,private_key"
            elif hd_name in [
                ElectrumV1HD.name(), ElectrumV2HD.name()
            ]:
                _show: str = "at:change,at:address,address,public_key,wif"
            elif hd_name == MoneroHD.name():
                _show: str = "at:minor,at:major,sub_address"
            else:
                raise Exception("Unknown HD")

            hdwallet_csv = csv.DictWriter(
                sys.stdout, fieldnames=_show.split(","), extrasaction="ignore", delimiter=kwargs.get("delimiter")
            )

            if kwargs.get("show_header"):
                hdwallet_csv.writeheader()

            def drive(*args) -> List[str]:
                def drive_helper(derivations, current_derivation: List[Tuple[int, bool]] = []) -> List[str]:
                    if not derivations:

                        derivation_name: str = hdwallet._derivation.name()
                        if derivation_name in [
                            BIP44Derivation.name(), BIP49Derivation.name(), BIP84Derivation.name(), BIP86Derivation.name()
                        ]:
                            _derivation: IDerivation = DERIVATIONS[derivation_name](
                                coin_type=current_derivation[1][0],
                                account=current_derivation[2][0],
                                change=current_derivation[3],
                                address=current_derivation[4][0]
                            )
                        elif derivation_name == CIP1852Derivation.name():
                            _derivation: IDerivation = DERIVATIONS[derivation_name](
                                coin_type=current_derivation[1][0],
                                account=current_derivation[2][0],
                                role=current_derivation[3],
                                address=current_derivation[4][0]
                            )
                        elif derivation_name == ElectrumDerivation.name():
                            _derivation: IDerivation = DERIVATIONS[derivation_name](
                                change=current_derivation[0][0],
                                address=current_derivation[1][0]
                            )
                        elif derivation_name == MoneroDerivation.name():
                            _derivation: IDerivation = DERIVATIONS[derivation_name](
                                minor=current_derivation[0][0],
                                major=current_derivation[1][0]
                            )
                        else:
                            _derivation: IDerivation = DERIVATIONS[derivation_name](
                                path="m/" + "/".join(
                                    [str(item[0]) + "'" if item[1] else str(item[0]) for item in current_derivation]
                                )
                            )

                        new_dump: dict = { }
                        hdwallet.update_derivation(
                            derivation=_derivation
                        )
                        dump: dict = hdwallet.dump(exclude={"root"})
                        for key in [keys.split(":") for keys in _show.split(",")]:
                            if len(key) == 2:
                                new_dump.setdefault(f"{key[0]}:{key[1]}", dump[key[0]][key[1]])
                            else:
                                new_dump.setdefault(f"{key[0]}", dump[key[0]])
                        hdwallet_csv.writerow(new_dump)
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

            if hdwallet._derivation is None:
                return None

            drive(*hdwallet._derivation.derivations())

        elif kwargs.get("format") == "json":
            click.echo(json.dumps(
                hdwallet.dumps(exclude=set(kwargs.get("exclude").split(","))), indent=4, ensure_ascii=False
            ))
        else:
            click.echo(click.style(
                f"Wrong format, (expected= json | csv, got='{kwargs.get('format')}')"
            ), err=True)
            sys.exit()

    except Exception as exception:
        click.echo(click.style(
            f"Error: {str(exception)}"
        ), err=True)
        sys.exit()
