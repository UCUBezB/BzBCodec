'''
TODO: rewrite via numpy so to increase the speed of execution
'''

from typing import List, Tuple, Dict

def lzw_compress(bitarray: List[int]) -> List[int]:
    '''
    Compresses an array of bits into smaller one
    '''

    dict_size: int = 256
    mapping_dict: Dict[Tuple[int], Tuple[int]] = {tuple([i,]): tuple([i,]) for i in range(dict_size)}

    current_word: List[int] = []
    res: List[int] = []
    for num in bitarray:
        next_word: Tuple[int] = tuple(current_word + [num])
        if next_word in mapping_dict:
            current_word = list(next_word)
        else:
            # print(res, tuple(current_word), mapping_dict[tuple(current_word)])
            res += mapping_dict[tuple(current_word)]
            mapping_dict[next_word] = tuple([dict_size, ])
            dict_size += 1
            current_word = [num]

    if current_word:
        res += current_word

    return res


def lzw_decompress(compressed: List[int]) -> List[int]:
    '''
    Decompresses an array of bits into smaller one
    '''

    dict_size: int = 256
    mapping_dict: Dict[int, Tuple[int]] = {i: tuple([i, ]) for i in range(dict_size)}
    
    res: List[int] = []
    current_word: int = compressed.pop(0)

    res += [current_word]

    for num in compressed:
        if num in mapping_dict:
            entry = mapping_dict[num]
        elif num == dict_size:
            entry = tuple([*current_word, current_word[0]])

        res += entry
        try:
            mapping_dict[dict_size] = tuple([*current_word, entry[0]])
        except TypeError:
            mapping_dict[dict_size] = tuple([current_word, entry[0]])

        current_word = entry
        dict_size += 1
    print(''.join([chr(elm) for elm in res]))
    return res


if __name__ == '__main__':
    ascii_msg = [ord(elm) for elm in 'TOBEORNOTTOBEORTOBEORNOT']
    print(ascii_msg)
    compressed = lzw_compress(ascii_msg)
    print(compressed)
    decompressed = lzw_decompress(compressed)
    print(decompressed)
    print(''.join([chr(elm) for elm in decompressed]))
