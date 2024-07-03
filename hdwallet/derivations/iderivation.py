#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Optional, List, Tuple, Union
)

from ..utils import normalize_derivation


class IDerivation:

    _path: str = "m/"
    _indexes: List[int] = []
    _derivations: List[Tuple[int, bool]] = { }

    def __init__(
        self, path: Optional[str] = None, indexes: Optional[List[int]] = None, **kwargs
    ) -> None:
        """
        Initializes an object for iderivation.

        :param path: Optional derivation path string.
        :type path: Optional[str]

        :param indexes: Optional list of derivation indexes.
        :type indexes: Optional[List[int]]

        :return: No return
        :rtype: NoneType
        """

        self._path, self._indexes, self._derivations = normalize_derivation(
            path=path, indexes=indexes
        )

    def __str__(self) -> str:
        """
        Return the string representation of the derivation path.

        :return: The derivation path as a string.
        :rtype: str

        >>> from {module_path} import {class_name}
        >>> derivation: {class_name} = {class_name}(derivation="...")
        >>> derivation.__str__()
        "..."
        """

        return self._path

    @classmethod
    def name(cls) -> str:
        pass

    def clean(self) -> "IDerivation":
        pass

    def path(self) -> str:
        """
        Retrieves the path associated with the current instance.

        :return: The derivation as a string.
        :rtype: str

        >>> from {module_path} import {class_name}
        >>> derivation: {class_name} = {class_name}(derivation="...")
        >>> derivation.path()
        "..."
        """

        return self._path

    def indexes(self) -> List[int]:
        """
        Retrieve the list of indexes in the derivation path.

        :return: A list of integer indexes used in the derivation path.
        :rtype: List[int]

        >>> from {module_path} import {class_name}
        >>> derivation: {class_name} = {class_name}(derivation="...")
        >>> derivation.indexes()
        ...
        """

        return self._indexes

    def derivations(self) -> List[Tuple[int, bool]]:
        """
        Retrieve the list of derivations in the derivation path.

        :return: A list of tuples where each tuple contains an index and a boolean indicating whether the index is hardened.
        :rtype: List[Tuple[int, bool]]

        >>> from {module_path} import {class_name}
        >>> derivation: {class_name} = {class_name}(derivation="...")
        >>> derivation.derivations()
        ...
        """

        return self._derivations

    def depth(self) -> int:
        """
        Retrieve the depth of the derivation path.

        :return: The number of derivation levels in the path.
        :rtype: int

        >>> from {module_path} import {class_name}
        >>> {class_name}.depth(derivation="...")
        ...
        """

        return len(self._derivations)

    def purpose(self) -> int:
        pass

    def coin_type(self) -> int:
        pass

    def account(self) -> int:
        pass

    def change(self) -> Union[int, str]:
        pass

    def role(self) -> str:
        pass

    def address(self) -> int:
        pass

    def minor(self) -> int:
        pass

    def major(self) -> int:
        pass
