import numpy as np
from time import time
from typing import Tuple, List

def compress(
        initial_input_array: np.array, max_offset: int=511, max_length: int=510
    ) -> List[Tuple[int, int, str]]:

    output = []

    buffer = np.array([], dtype=np.int16)
    input_array = initial_input_array

    current_cut_position = 0

    print_i = 0
    while len(input_array) != 0:
        print_i += 1
        if print_i % 100 == 0:
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
    return min_len if len(not_equal_indexes) == 0 else not_equal_indexes[0]

def best_length_offset(
        buffer: np.array, input_array: np.array,
        max_length: int=15, max_offset: int=4095
    ) -> Tuple[int, int]:

    if max_offset < len(buffer):
        cut_buffer = buffer[-max_offset:]
    else:
        cut_buffer = buffer

    if input_array is None or len(input_array) == 0:
        return 0

    length, offset = (1, 0)

    if input_array[0] not in cut_buffer:
        best_length = input_array[0] == input_array[1]
        return min(
            (length + best_length), max_length
        ), offset

    length = 0

    for index in range(1, len(cut_buffer) + 1):
        char = cut_buffer[-index]
        if char == input_array[0]:

            found_offset = index
            found_length = repeating_length_from_start(cut_buffer[-index:], input_array)

            if found_length > length:
                length = found_length
                offset = found_offset
        

    return min(length, max_length), offset


