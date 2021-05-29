'''
TODO: rewrite via numpy so to increase the speed of execution
'''

import numpy as np
from typing import List, Tuple, Dict

def lzw_compress(bitarray: np.array) -> np.array:
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

    return np.array(res)


def lzw_decompress(compressed: np.array) -> np.array:
    '''
    Decompresses an array of bits into smaller one
    '''

    dict_size: int = 256
    mapping_dict: Dict[int, Tuple[int]] = {i: tuple([i, ]) for i in range(dict_size)}
    
    res: List[int] = []
    compressed = list(compressed)
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
    return np.array(res)


if __name__ == '__main__':
    ascii_msg = [ord(elm) for elm in 'Sed ut perspiciatis, unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam eaque ipsa, quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt, explicabo. Nemo enim ipsam voluptatem, quia voluptas sit, aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos, qui ratione voluptatem sequi nesciunt, neque porro quisquam est, qui dolorem ipsum, quia dolor sit, amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt, ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit, qui in ea voluptate velit esse, quam nihil molestiae consequatur, vel illum, qui dolorem eum fugiat, quo voluptas nulla pariatur? [33] At vero eos et accusamus et iusto odio dignissimos ducimus, qui blanditiis praesentium voluptatum deleniti atque corrupti, quos dolores et quas molestias excepturi sint, obcaecati cupiditate non provident, similique sunt in culpa, qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio, cumque nihil impedit, quo minus id, quod maxime placeat, facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet, ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.']
    # print(ascii_msg)
    print(len(ascii_msg))
    compressed = lzw_compress(ascii_msg)
    # print(compressed)
    print(len(compressed))
    decompressed = lzw_decompress(compressed)
    # print(decompressed)
    assert list(decompressed) == list(ascii_msg)
    # print(''.join([chr(elm) for elm in decompressed]))
