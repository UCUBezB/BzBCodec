'''
LZ77 Compression alghorithm.

TODO: Please consider wrapping it up into a class
'''

import numpy as np
from time import time
from typing import Tuple, List

def compress(
        initial_input_array: np.array, max_offset: int=128, max_length: int=65536
    ) -> List[Tuple[int, int, str]]:

    output = []

    buffer = np.array([])
    input_array = initial_input_array

    current_cut_position = 0

    print_i = 0
    while len(input_array) != 0:
        print_i += 1
        if print_i % 1000 == 0:
            print(current_cut_position, end='    \r')
        length, offset = best_length_offset(buffer, input_array, max_length, max_offset)
        output.append((offset, length, input_array[0]))
        current_cut_position += length
        buffer = initial_input_array[:current_cut_position]
        input_array = initial_input_array[current_cut_position:]

    return output


def repeating_length_from_start(buffer: np.array, input_array: np.array):
    '''
    Return the repeating length of the input array from the start of buffer.
    '''
    min_len = min(len(buffer), len(input_array))
    not_equal_indexes = np.flatnonzero(buffer[:min_len] != input_array[:min_len])
    if len(not_equal_indexes) == 0:
        length_delta = 0
        while len(not_equal_indexes) == 0:
            if len(buffer) < len(input_array):
                length_delta += min_len
                input_array = input_array[min_len:]
                min_len = min(len(buffer), len(input_array))
                not_equal_indexes = np.flatnonzero(buffer[:min_len] != input_array[:min_len])
            else:
                return min_len + length_delta
        return not_equal_indexes[0] + length_delta
    else:
        return not_equal_indexes[0]


def best_length_offset(
        buffer: np.array, input_array: np.array,
        max_length: int=15, max_offset: int=4095
    ) -> Tuple[int, int]:

    cut_buffer = buffer[-max_offset:]

    if input_array[0] not in cut_buffer:
        for i in range(10):
            if not (len(input_array) > (i + 1) and input_array[i + 1] == input_array[i]):
                best_length = i
                break
        else:
            input_array = input_array[:max_length]
            not_equal_indexes = np.flatnonzero(input_array[1:] != input_array[0])
            best_length = max(len(input_array) - 1, 0) if len(not_equal_indexes) == 0 else not_equal_indexes[0]
        return min(
            best_length + 1, max_length
        ), 0

    input_array = input_array[:max_length]

    length, offset = 0, 0

    for index in range(len(cut_buffer), 0, -1):

        char = cut_buffer[-index]
        if char == input_array[0]:

            found_length = repeating_length_from_start(cut_buffer[-index:], input_array)

            if found_length > length:
                length = found_length
                offset = index

                # break  # uncomment for fast (but uneffective) convertion video

                if length >= len(input_array):
                    # we won't find anything better
                    break

    return min(length, max_length), offset


def array_size(compressed_array: list) -> int:
    '''
    Return size of array before compression.
    '''

    return sum(list(zip(*compressed_array))[1])


def decompress(compressed: List[Tuple[int, int, int]]) -> np.array:
    '''
    Decompress array.
    '''
    arr_size = array_size(compressed)
    decompressed_array = np.zeros(arr_size)
    current_index = 0
    for value in compressed:
        offset, length, char = value
        if offset == 0:
            decompressed_array[current_index:current_index+length] = char
            current_index += length
        else:
            while length >= offset:
                decompressed_array[
                    current_index:current_index + offset
                ] = decompressed_array[current_index-offset:current_index]
                current_index += offset
                length -= offset
            decompressed_array[
                current_index:current_index + length
            ] = decompressed_array[current_index-offset:current_index-offset+length]
            current_index += length

    return decompressed_array

if __name__ == "__main__":
    for name in ['examples/test_img.bzbi']:
        print(name, end=':\n')
        img = np.load(name, allow_pickle=True)[0]
        print(len(img))
        t = time()
        img_comp = compress(img)
        print(img_comp)
        print(len(img_comp), end='        \n')
        print(time() - t)
        print(np.all(decompress(img_comp) == img))
