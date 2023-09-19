#!/usr/bin/env python3

from abc import (
    ABC, abstractmethod
)


class ISeed(ABC):

    @classmethod
    @abstractmethod
    def generate(cls, mnemonic: str) -> str:
        pass
