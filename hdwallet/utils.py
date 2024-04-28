#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from random import choice
from typing import (
    List, Tuple, AnyStr, Optional, Union, Literal
)

import binascii
import string
import re

from .exceptions import DerivationError


def generate_passphrase(length: int = 32) -> str:
    return "".join(choice(string.ascii_letters + string.digits) for _ in range(length))


def get_hmac(ecc_name: str) -> bytes:
    if ecc_name in [
        "Kholaw-Ed25519", "SLIP10-Ed25519", "SLIP10-Ed25519-Blake2b", "SLIP10-Ed25519-Monero"
    ]:
        return b"ed25519 seed"
    elif ecc_name == "SLIP10-Nist256p1":
        return b"Nist256p1 seed"
    elif ecc_name == "SLIP10-Secp256k1":
        return b"Bitcoin seed"


def exclude_keys(nested: dict, keys: set) -> dict:
    new: dict = { }
    for _key, _value in nested.items():
        if isinstance(_value, dict):
            new[_key] = exclude_keys(_value, keys)
        elif _key not in [key.replace("-", "_") if isinstance(key, str) else key for key in keys]:
            new[_key] = _value
    return new


def path_to_indexes(path: str) -> List[int]:

    if path in ["m", "m/"]:
        return []
    elif path[0:2] != "m/":
        raise DerivationError(
            f"Bad path format", expected="like this type of path \"m/0'/0\"", got=path
        )

    indexes: List[int] = []
    for index in path.lstrip("m/").split("/"):
        indexes.append((int(index[:-1]) + 0x80000000) if "'" in index else int(index))
    return indexes


def indexes_to_path(indexes: List[int]) -> str:

    path: str = "m"
    for index in indexes:
        path += f"/{index - 0x80000000}'" if index & 0x80000000 else f"/{index}"
    return path


def normalize_index(
    index: Union[str, int, Tuple[int, int]], hardened: bool = False
) -> Union[Tuple[int, bool], Tuple[int, int, bool]]:

    if isinstance(index, tuple):
        if len(index) != 2:
            raise DerivationError(
                f"Bad index length", expected=2, got=len(index)
            )
        elif not isinstance(index[0], int) or not isinstance(index[1], int):
            raise DerivationError(
                f"Invalid index types",
                expected="both indexes must be integer instance",
                got=f"{type(index[0])}-{type(index[0])}"
            )
        elif index[0] < 0 or index[1] < 0:
            raise DerivationError(
                f"Bad index format", expected="both must be non-negative-numbers", got=index
            )
        elif index[0] > index[1]:
            raise DerivationError(
                f"Bad index, from {index[0]} index should be less than to {index[1]} index"
            )
        return *index, hardened

    elif isinstance(index, str):

        match: re.Match = re.match(
            r"^(\d+)(-(\d+))?$", index
        )
        if match:
            from_index: int = int(match.group(1))
            to_index: Optional[int] = (
                int(match.group(3)) if match.group(3) else None
            )
            if to_index is None:
                return from_index, hardened
            if from_index > to_index:
                raise DerivationError(
                    f"Bad index, from {from_index} index should be less than to {to_index} index"
                )
            return from_index, to_index, hardened
        raise DerivationError(
            f"Bad index format", expected="{non-negative-number} | {number}-{number}", got=index
        )

    elif isinstance(index, int):
        if index < 0:
            raise DerivationError(
                f"Bad index format", expected="non-negative-number", got=index
            )
        return index, hardened

    raise DerivationError(
        f"Invalid index instance", expected=(str, int, tuple), got=type(index)
    )


def normalize_derivation(
    path: Optional[str] = None, indexes: Optional[List[int]] = None
) -> Tuple[str, List[int], List[tuple]]:

    _path: str = "m"
    _indexes: List[int] = []
    _derivations: List[tuple] = []

    if indexes:
        path = indexes_to_path(indexes=indexes)
    elif path:
        if path in ["m", "m/"]:
            return f"{_path}/", _indexes, _derivations
        elif path[0:2] != "m/":
            raise DerivationError(
                f"Bad path format", expected="like this type of path \"m/0'/0\"", got=path
            )
    elif not path:
        return f"{_path}/", _indexes, _derivations

    for depth, index in enumerate(path.lstrip("m/").split("/")):
        if "'" in index:
            if "-" in index:
                _from_index, _to_index = index[:-1].split("-")
                _index: int = int(_to_index)
                if int(_from_index) >= int(_to_index):
                    raise DerivationError(
                        f"On {depth} depth, the starting {_from_index} must be less than the ending {_to_index} index"
                    )
                _derivations.append((int(_from_index), int(_to_index), True))
            else:
                _index: int = int(index[:-1])
                _derivations.append((_index, True))
            _indexes.append(_index + 0x80000000)
            _path += f"/{_index}'"
        else:
            if "-" in index:
                _from_index, _to_index = index.split("-")
                _index: int = int(_to_index)
                if int(_from_index) >= int(_to_index):
                    raise DerivationError(
                        f"On {depth} depth, the starting {_from_index} must be less than the ending {_to_index} index"
                    )
                _derivations.append((int(_from_index), int(_to_index), False))
            else:
                _index: int = int(index)
                _derivations.append((_index, False))
            _indexes.append(_index)
            _path += f"/{_index}"

    return _path, _indexes, _derivations


def index_tuple_to_integer(index: Union[Tuple[int, bool], Tuple[int, int, bool]]) -> int:
    if not isinstance(index, tuple):
        raise DerivationError("Invalid index instance", expected=tuple, got=type(index))
    elif len(index) == 3:
        return (index[1] + 0x80000000) if index[2] else index[0]
    elif len(index) == 2:
        return (index[0] + 0x80000000) if index[1] else index[0]
    raise DerivationError("Wrong index length", expected=[2, 3], got=len(index))


def index_tuple_to_string(index: Union[Tuple[int, bool], Tuple[int, int, bool]]) -> str:
    if not isinstance(index, tuple):
        raise DerivationError("Invalid index instance", expected=tuple, got=type(index))
    elif len(index) == 3:
        _from_index, _to_index, _hardened = index[0], index[1], "'" if index[2] else ""
        return f"{_from_index}-{_to_index}{_hardened}"
    elif len(index) == 2:
        _index, _hardened = index[0], "'" if index[1] else ""
        return f"{_index}{_hardened}"
    raise DerivationError("Wrong index length", expected=[2, 3], got=len(index))


def index_string_to_tuple(index: str) -> Tuple[int, bool]:
    index_split: List[str] = index.split("'")
    return (
        (int(index_split[0]), True)
        if index.endswith("'") else
        (int(index_split[0]), False)
    )


def xor(data_1: bytes, data_2: bytes) -> bytes:
    return bytes(
        [b1 ^ b2 for b1, b2 in zip(data_1, data_2)]
    )


def add_no_carry(data_1: bytes, data_2: bytes) -> bytes:
    return bytes(
        [(b1 + b2) & 0xFF for b1, b2 in zip(data_1, data_2)]
    )


def multiply_scalar_no_carry(data: bytes, scalar: int) -> bytes:
    return bytes(
        [(b * scalar) & 0xFF for b in data]
    )


def is_bits_set(value: int, bit_num: int) -> bool:
    return (value & (1 << bit_num)) != 0


def are_bits_set(value: int, bit_mask: int) -> bool:
    return (value & bit_mask) != 0


def set_bit(value: int, bit_num: int) -> int:
    return value | (1 << bit_num)


def set_bits(value: int, bit_mask: int) -> int:
    return value | bit_mask


def reset_bit(value: int, bit_num: int) -> int:
    return value & ~(1 << bit_num)


def reset_bits(value: int, bit_mask: int) -> int:
    return value & ~bit_mask


def get_bytes(data: AnyStr, unhexlify: bool = True) -> bytes:
    if not data:
        return b''
    if isinstance(data, bytes):
        return data
    elif isinstance(data, str):
        if unhexlify:
            return bytes.fromhex(data)
        else:
            return bytes(data, 'utf-8')
    else:
        raise TypeError("Agreement must be either 'bytes' or 'string'!")


def bytes_reverse(data: bytes) -> bytes:
    tmp = bytearray(data)
    tmp.reverse()
    return bytes(tmp)


def bytes_to_string(data: Union[bytes, str]) -> str:
    if not data:
        return ''
    try:
        bytes.fromhex(data)
        return data
    except (ValueError, TypeError):
        pass
    if not isinstance(data, bytes):
        data = bytes(data, 'utf-8')
    return data.hex()


def bytes_to_integer(data: bytes, endianness: Literal["little", "big"] = "big", signed: bool = False) -> int:
    return int.from_bytes(data, byteorder=endianness, signed=signed)


def integer_to_bytes(data: int, bytes_num: Optional[int] = None, endianness: Literal["little", "big"] = "big", signed: bool = False) -> bytes:
    bytes_num = bytes_num or ((data.bit_length() if data > 0 else 1) + 7) // 8
    return data.to_bytes(bytes_num, byteorder=endianness, signed=signed)


def integer_to_binary_string(data: int, zero_pad_bit_len: int = 0) -> str:
    return bin(data)[2:].zfill(zero_pad_bit_len)


def binary_string_to_integer(data: Union[bytes, str]) -> int:
    return int((data.encode("utf-8") if isinstance(data, str) else data), 2)


def bytes_to_binary_string(data: bytes, zero_pad_bit_len: int = 0) -> str:
    return integer_to_binary_string(bytes_to_integer(data), zero_pad_bit_len)


def binary_string_to_bytes(data: Union[bytes, str], zero_pad_byte_len: int = 0) -> bytes:
    return binascii.unhexlify(hex(binary_string_to_integer(data))[2:].zfill(zero_pad_byte_len))


def decode(data: Union[bytes, str], encoding: str = "utf-8") -> str:

    if isinstance(data, str):
        return data
    if isinstance(data, bytes):
        return data.decode(encoding)
    raise TypeError("Invalid data type")


def encode(data: Union[bytes, str], encoding: str = "utf-8") -> bytes:

    if isinstance(data, str):
        return data.encode(encoding)
    if isinstance(data, bytes):
        return data
    raise TypeError("Invalid data type")


def convert_bits(
    data: Union[bytes, List[int]], from_bits: int, to_bits: int
) -> Optional[List[int]]:

    max_out_val = (1 << to_bits) - 1

    acc = 0
    bits = 0
    ret = []

    for value in data:
        if value < 0 or (value >> from_bits):
            return None
        acc |= value << bits
        bits += from_bits
        while bits >= to_bits:
            ret.append(acc & max_out_val)
            acc = acc >> to_bits
            bits -= to_bits

    if bits != 0:
        ret.append(acc & max_out_val)

    return ret


def bytes_chunk_to_words(
    bytes_chunk: bytes, words_list: List[str], endianness: Literal["little", "big"]
) -> List[str]:

    words_list_length = len(words_list)

    chunk: int = bytes_to_integer(bytes_chunk, endianness=endianness)

    word_1_index = chunk % words_list_length
    word_2_index = ((chunk // words_list_length) + word_1_index) % words_list_length
    word_3_index = ((chunk // words_list_length // words_list_length) + word_2_index) % words_list_length

    return [words_list[index] for index in (word_1_index, word_2_index, word_3_index)]


def words_to_bytes_chunk(
    word_1: str, word_2: str, word_3: str, words_list: List[str], endianness: Literal["little", "big"]
) -> bytes:

    words_list_length = len(words_list)
    words_list_with_index: dict = {
        words_list[i]: i for i in range(len(words_list))
    }

    word_1_index, word_2_index,  word_3_index = (
        words_list_with_index[word_1], words_list_with_index[word_2] % words_list_length, words_list_with_index[word_3] % words_list_length
    )

    chunk: int = (
        word_1_index + (
            words_list_length * ((word_2_index - word_1_index) % words_list_length)
        ) + (
            words_list_length * words_list_length * ((word_3_index - word_2_index) % words_list_length)
        )
    )

    return integer_to_bytes(
        chunk, bytes_num=4, endianness=endianness
    )
