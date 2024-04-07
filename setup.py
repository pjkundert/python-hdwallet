#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from setuptools import (
    setup, find_packages
)

import importlib.util

# README.md
with open("README.md", "r", encoding="utf-8") as readme:
    long_description: str = readme.read()

# requirements.txt
with open("requirements.txt", "r") as _requirements:
    requirements: list = list(map(str.strip, _requirements.read().split("\n")))

# hdwallet/info.py
spec = importlib.util.spec_from_file_location(
    "info", "hdwallet/info.py"
)
info = importlib.util.module_from_spec(spec)
spec.loader.exec_module(info)

setup(
    name=info.__name__,
    version=info.__version__,
    description=info.__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=info.__license__,
    author=info.__author__,
    author_email=info.__email__,
    url=info.__url__,
    project_urls={
        "Tracker": info.__tracker__,
        "Documentation": info.__docs__
    },
    keywords=info.__keywords__,
    entry_points={
        "console_scripts": ["hdwallet=hdwallet.cli.__main__:cli_main"]
    },
    python_requires=">=3.6,<4",
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        "cli": [
            "click>=8.1.3,<9",
            "click-aliases>=1.0.1,<2",
            "tabulate>=0.9.0,<1"
        ],
        "tests": [
            "pytest>=7.2.0,<8",
            "pytest-cov>=4.0.0,<5",
            "tox==3.28.0"
        ],
        "docs": [
            "sphinx>=5.3.0,<6",
            "furo==2022.12.7",
            "sphinx-click>=4.4.0,<5"
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
