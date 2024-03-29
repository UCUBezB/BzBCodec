import numpy as np
from typing import List, Tuple, Dict

def lzw_compress(data: np.array) -> np.array:
    '''
    Compresses an array of bits into smaller one
    '''

    dict_size: int = 256
    mapping_dict: Dict[str, int] = {str(i): i for i in range(dict_size)}

    current_word: str = ''
    res: List[int] = []
    for num in data:
        next_word: Tuple[int] = f'{current_word}{num}'
        if next_word in mapping_dict:
            current_word = next_word
        else:
            res.append(mapping_dict[current_word])
            mapping_dict[next_word] = dict_size
            dict_size += 1
            current_word = str(num)

    if current_word:
        res.append(mapping_dict[current_word])

    return np.array(res)


def lzw_decompress(compressed: np.array) -> np.array:
    '''
    Decompresses an array of bits into smaller one
    '''

    dict_size: int = 256
    mapping_dict: Dict[int, str] = {i: tuple([i]) for i in range(dict_size)}

    res: List[int] = []
    compressed = compressed.tolist()
    current_word: int = compressed.pop(0)

    res += [current_word]
    for num in compressed:
        if num in mapping_dict:
            entry = mapping_dict[num]
        else:
            entry = tuple([*current_word, current_word[0]]) if not isinstance(current_word, int) \
                                                        else tuple([current_word, current_word])
        res += entry
        try:
            mapping_dict[dict_size] = tuple([*current_word, entry[0]])
        except TypeError:
            mapping_dict[dict_size] = tuple([current_word, entry[0]])

        current_word = entry
        dict_size += 1

    return np.array(res)


if __name__ == '__main__':
    # --------------------------------------------------------------------------------
    # Usage with text
    # --------------------------------------------------------------------------------
    ascii_msg = [ord(elm) for elm in 'Sed ut perspiciatis, unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam eaque ipsa, quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt, explicabo. Nemo enim ipsam voluptatem, quia voluptas sit, aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos, qui ratione voluptatem sequi nesciunt, neque porro quisquam est, qui dolorem ipsum, quia dolor sit, amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt, ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit, qui in ea voluptate velit esse, quam nihil molestiae consequatur, vel illum, qui dolorem eum fugiat, quo voluptas nulla pariatur? [33] At vero eos et accusamus et iusto odio dignissimos ducimus, qui blanditiis praesentium voluptatum deleniti atque corrupti, quos dolores et quas molestias excepturi sint, obcaecati cupiditate non provident, similique sunt in culpa, qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio, cumque nihil impedit, quo minus id, quod maxime placeat, facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet, ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.']
    from time import time
    start_time = time()
    compressed = lzw_compress(np.array(ascii_msg))
    decompressed = lzw_decompress(compressed)
    assert list(decompressed) == list(ascii_msg)
    print(f'Compression and decompression has taken {time() - start_time}')

    # --------------------------------------------------------------------------------
    # Usage with image
    # --------------------------------------------------------------------------------
    from PIL import Image
    np.set_printoptions(threshold=np.inf)
    img = Image.open('examples/test_img.png').convert('RGB')
    img = np.array(img.getdata())
    img = np.ravel(img)
    start_time = time()
    compressed = lzw_compress(img)
    decompressed = lzw_decompress(compressed)
    print(f'Compression and decompression has taken {time() - start_time}')
    assert np.all(img == decompressed)
