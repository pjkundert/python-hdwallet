#!/usr/bin/env python3

from typing import (
    List, Optional, Literal, Union
)

from ..utils import (
    integer_to_bytes, bytes_to_integer
)


def convert_bits(
    data: Union[bytes, List[int]], from_bits: int, to_bits: int
) -> Optional[List[int]]:

    max_out_val = (1 << to_bits) - 1

    acc = 0
    bits = 0
    ret = []

    for value in data:
        # Value shall not be less than zero or greater than 2^from_bits
        if value < 0 or (value >> from_bits):
            return None
        # Continue accumulating until greater than to_bits
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

    # Get the word indexes
    word_1_index, word_2_index,  word_3_index = (
        words_list_with_index[word_1], words_list_with_index[word_2] % words_list_length, words_list_with_index[word_3] % words_list_length
    )

    # Get back the bytes chunk
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
