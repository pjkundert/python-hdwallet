bip_44_to_bip_144_rule = {
        "available-methods": {
            "entropy": {
                "method": "entropy",
                "derivable": True,
            },
            "mnemonic": {
                "method": "mnemonic",
                "derivable": True
            },
            "seed": {
                "method": "seed",
                "derivable": True,
                "root-changes": {
                    "entropy": None,
                    "strength": None,
                    "mnemonic": None,
                    "passphrase": None,
                    "language": None
                }
            },
            "xprivate-key": {
                "method": "root_xprivate_key",
                "derivable": True,
                "root-changes": {
                    "entropy": None,
                    "strength": None,
                    "mnemonic": None,
                    "passphrase": None,
                    "language": None,
                    "seed": None
                }
            },
            "wif": {
                "method": "wif",
                "derivable": False,
                "root-changes": {
                    "entropy": None,
                    "strength": None,
                    "mnemonic": None,
                    "passphrase": None,
                    "language": None,
                    "seed": None,
                    "root_xprivate_key": None,
                    "root_xpublic_key": None,
                    "root_private_key": None,
                    "root_wif": None,
                    "root_chain_code": None,
                    "root_public_key": None,
                    "strict": None
                },
                "derivation-changes": {
                    "xprivate_key": None,
                    "xpublic_key": None,
                    "chain_code": None,
                    "parent_fingerprint": None
                }
            },
            "private-key": {
                "method": "private_key",
                "derivable": False,
                "root-changes": {
                    "entropy": None,
                    "strength": None,
                    "mnemonic": None,
                    "passphrase": None,
                    "language": None,
                    "seed": None,
                    "root_xprivate_key": None,
                    "root_xpublic_key": None,
                    "root_private_key": None,
                    "root_wif": None,
                    "root_chain_code": None,
                    "root_public_key": None,
                    "strict": None
                },
                "derivation-changes": {
                    "xprivate_key": None,
                    "xpublic_key": None,
                    "chain_code": None,
                    "parent_fingerprint": None
                }
            },
            "public-key": {
                "method": "public_key",
                "derivable": False,
                "root-changes": {
                    "entropy": None,
                    "strength": None,
                    "mnemonic": None,
                    "passphrase": None,
                    "language": None,
                    "seed": None,
                    "root_xprivate_key": None,
                    "root_xpublic_key": None,
                    "root_private_key": None,
                    "root_wif": None,
                    "root_chain_code": None,
                    "root_public_key": None,
                    "wif_type": None,
                    "strict": None
                },
                "derivation-changes": {
                    "xprivate_key": None,
                    "xpublic_key": None,
                    "private_key": None,
                    "chain_code": None,
                    "wif": None,
                    "parent_fingerprint": None
                }
            }
        },
        "args": {
            "public-key-type": "public_key_type",
            "language": "language"
        }
    }

rules = {
    "BIP32" : {
        "available-methods": {
            "entropy": {
                "method": "entropy",
                "derivable": True,
            },
            "mnemonic": {
                "method": "mnemonic",
                "derivable": True
            },
            "seed": {
                "method": "seed",
                "derivable": True,
                "root-changes": {
                    "entropy": None,
                    "strength": None,
                    "mnemonic": None,
                    "passphrase": None,
                    "language": None
                }
            },
            "xprivate-key": {
                "method": "root_xprivate_key",
                "derivable": True,
                "root-changes": {
                    "entropy": None,
                    "strength": None,
                    "mnemonic": None,
                    "passphrase": None,
                    "language": None,
                    "seed": None
                }
            },
            "xpublic-key": {
                "method": "root_xpublic_key",
                "derivable": True,
                "root-changes": {
                    "entropy": None,
                    "strength": None,
                    "mnemonic": None,
                    "passphrase": None,
                    "language": None,
                    "seed": None,
                    "root_xprivate_key": None,
                    "root_private_key": None,
                    "root_wif": None,
                    "wif_type": None
                },
                "derivation-changes": {
                    "xprivate_key": None,
                    "private_key": None,
                    "wif": None
                }
            },
            "wif": {
                "method": "wif",
                "derivable": False,
                "root-changes": {
                    "entropy": None,
                    "strength": None,
                    "mnemonic": None,
                    "passphrase": None,
                    "language": None,
                    "seed": None,
                    "root_xprivate_key": None,
                    "root_xpublic_key": None,
                    "root_private_key": None,
                    "root_wif": None,
                    "root_chain_code": None,
                    "root_public_key": None,
                    "strict": None
                },
                "derivation-changes": {
                    "xprivate_key": None,
                    "xpublic_key": None,
                    "chain_code": None,
                    "parent_fingerprint": None
                }
            },
            "private-key": {
                "method": "private_key",
                "derivable": False,
                "root-changes": {
                    "entropy": None,
                    "strength": None,
                    "mnemonic": None,
                    "passphrase": None,
                    "language": None,
                    "seed": None,
                    "root_xprivate_key": None,
                    "root_xpublic_key": None,
                    "root_private_key": None,
                    "root_wif": None,
                    "root_chain_code": None,
                    "root_public_key": None,
                    "strict": None
                },
                "derivation-changes": {
                    "xprivate_key": None,
                    "xpublic_key": None,
                    "chain_code": None,
                    "parent_fingerprint": None
                }
            },
            "public-key": {
                "method": "public_key",
                "derivable": False,
                "root-changes": {
                    "entropy": None,
                    "strength": None,
                    "mnemonic": None,
                    "passphrase": None,
                    "language": None,
                    "seed": None,
                    "root_xprivate_key": None,
                    "root_xpublic_key": None,
                    "root_private_key": None,
                    "root_wif": None,
                    "root_chain_code": None,
                    "root_public_key": None,
                    "wif_type": None,
                    "strict": None
                },
                "derivation-changes": {
                    "xprivate_key": None,
                    "xpublic_key": None,
                    "private_key": None,
                    "chain_code": None,
                    "wif": None,
                    "parent_fingerprint": None
                }
            }
        },
        "args": {
            "public-key-type": "public_key_type",
            "language": "language"
        }
    },
    "BIP44" : bip_44_to_bip_144_rule,
    "BIP49" : bip_44_to_bip_144_rule,
    "BIP84" : bip_44_to_bip_144_rule,
    "BIP86" : bip_44_to_bip_144_rule,
    "BIP141" : bip_44_to_bip_144_rule,
    "Cardano": {
        "available-methods": {
            "entropy": {
                "method": "entropy",
                "derivable": True,
            },
            "mnemonic": {
                "method": "mnemonic",
                "derivable": True
            },
            "seed": {
                "method": "seed",
                "derivable": True,
                "root-changes": {
                    "entropy": None,
                    "strength": None,
                    "mnemonic": None,
                    "passphrase": None,
                    "language": None
                }
            },
            "xprivate-key": {
                "method": "root_xprivate_key",
                "derivable": True,
                "root-changes": {
                    "entropy": None,
                    "strength": None,
                    "mnemonic": None,
                    "passphrase": None,
                    "language": None,
                    "seed": None
                }
            }
        },
        "args": {
            "cardano-type": "cardano_type",
            "language": "language",
            "seed-name": ("Cardano",),
            "address-type": ("staking",)
        }
    },
    "Electrum-V1": {
        "available-methods": {
            "entropy": {
                "method": "entropy",
                "derivable": True,
            },
            "mnemonic": {
                "method": "mnemonic",
                "derivable": True
            },
            "seed": {
                "method": "seed",
                "derivable": True,
                "root-changes": {
                    "entropy": None,
                    "strength": None,
                    "mnemonic": None,
                    "passphrase": None,
                    "language": None
                }
            },
            "wif": {
                "method": "wif",
                "derivable": True,
                "root-changes": {
                    "entropy": None,
                    "strength": None,
                    "mnemonic": None,
                    "passphrase": None,
                    "language": None,
                    "seed": None
                }
            },
            "master-private-key": {
                "method": "master_private_key",
                "derivable": True,
                "root-changes": {
                    "entropy": None,
                    "strength": None,
                    "mnemonic": None,
                    "passphrase": None,
                    "language": None,
                    "seed": None
                }
            },
            "master-public-key": {
                "method": "master_public_key",
                "derivable": False,
                "root-changes": {
                    "entropy": None,
                    "strength": None,
                    "mnemonic": None,
                    "passphrase": None,
                    "language": None,
                    "seed": None,
                    "master_private_key": None,
                    "master_wif": None,
                    "wif_type": None
                },
                "derivation-changes": {
                    "private_key": None,
                    "wif": None
                }
            }
        },
        "args": {
            "public-key-type": "public_key_type",
            "language": "language"
        }
    },
    "Monero": {
        "available-methods": {
            "entropy": {
                "method": "entropy",
                "derivable": True,
            },
            "mnemonic": {
                "method": "mnemonic",
                "derivable": True
            },
            "seed": {},
            "spend-private-key": {},
            "watch-only": {}
        },
        "args": {
            "language": "language",
            "payment-id": ("ad17dc6e6793d178",)
        }
    }
}
