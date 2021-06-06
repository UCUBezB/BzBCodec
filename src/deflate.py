import numpy as np
import sys
from itertools import chain
from typing import List
from src.lz77 import compress, decompress
from src.Huffman_algo import HuffmanCode

class Deflate:
    '''
    Simple realisation of Deflate coding algorithm, which is based on
    LZ77 and Huffman compression algos.
    '''

    def encode(self, data: np.array) -> np.array:
        '''
        Encodes the data using LZ77 and Huffman codding

        According to the specification, for each chunk of data, encoded data
        should foolow its huffman dict (created separately for it). Has two modes of
        encoding:
            - with dynamically created Huffman trees
            - no encoding for chunks with a little amound of redundant data
        Fixed Huffman trees were omitted as they were developed mainly for text, and
        according to our tests, they work not that fine for other types of data
        '''


        # ------ chunking the data ------
        сhunks: List[str] = []
        idx: int = 0
        while idx <= len(data):
            try:
                сhunks.append(data[idx:idx+65535])
            except IndexError:
                сhunks.append(data[idx:])
            idx += 65535

        res = []
        for chunk in сhunks:
            # ---- coding via lz77 --------
            codewords = compress(chunk)
            # print(f'During encoding {np.array(list([list(elm) for elm in codewords]))}')

            # --- encodes literals_and_distances and lengths separately ----
            literals_and_distances = [(elm[0], elm[-1]) for elm in codewords]
            lengths = [elm[1] for elm in codewords]
            encoded_lengths, lengths_table = HuffmanCode(lengths).encode()
            encoded_literals_and_distances, \
                literals_and_distances_table = HuffmanCode(list(chain(*literals_and_distances))).encode()
            # according to the specification, for each chunk of data, encoded data
            # should foolow its huffman dict (created separately for it)
            encoding_type = 1
            if len(encoded_lengths) + len(encoded_literals_and_distances) > len(chunk) * 5:
                encoding_type = 0
            
            if encoding_type:
                # if the chunk should be encoded with dynamically created huffman tree
                encoded_chunk = (1, lengths_table, encoded_lengths,\
                            literals_and_distances_table, encoded_literals_and_distances)
            else: # if the chunk should not be encoded
                encoded_chunk = (0, chunk)
            res.append(encoded_chunk)
            
        ov_size: int = 0
        # we count len because it returns list of 1 and 0, which then can be written
        # directly in binary file via python's struct module (struct.pack())
        for elm in res:
            if elm[0] == 0:
                ov_size += len(elm[1])
            elif elm[0] == 1:
                ov_size += len(elm[2]) + len(elm[4]) + sys.getsizeof(elm[1]) + sys.getsizeof(elm[3])
        
        print(f'Overall size of compression with deflate is: {ov_size}')
    
        return res
    

    def decode(self, compressed_data: np.array) -> np.array:
        '''
        Decodes the message, using the decode-implementation of LZ77 and Huffman.

        Takes: compressed data in np.array([List[int]]) format.
        '''

        res = []
        for chunk in compressed_data:
            # if the chunk was not compressed
            if chunk[0] == 0:
                res += list(chunk[1])
                continue
            
            # decoding huffman trees
            _, distances_table, distances_code, literals_table, literals_code = chunk
            literals = HuffmanCode(literals_code).decode(literals_table)
            literals = list(zip(literals[0::2], literals[1::2]))
            distances = HuffmanCode(distances_code).decode(distances_table)
            
            # preparing struct for lz77 decoding
            data_for_lz77 = []
            for idx, literal in enumerate(literals):
                elm = list(literal)
                elm.insert(1, distances[idx])
                data_for_lz77.append(tuple(elm))
                

            decoded_chunk = decompress(np.array(data_for_lz77, dtype=[
            ('offset', 'int64'), ('length', 'int64'),
            ('value', 'int64')
            ]))

            res += list(decoded_chunk)

            
        return np.array(res)


if __name__ == '__main__':
    d = Deflate()
    # -------- text usage example -----------
    msg = np.array([ord(elm) for elm in 'TOBEORNOTTOBEORTOBEORNOT'])
    print(f'Initial message: {msg}. Its lenght is: {len(msg)}')
    d = Deflate()
    encoded_data = d.encode(msg)

    res = d.decode(encoded_data)
    print(f'Message after coding and decoding: {res}')
    assert list(msg) == list(res)

    # -------- image usage example ----------
    print()
    from PIL import Image
    img = Image.open('examples/test_img.png').convert('RGB')
    img = np.array(img.getdata())
    img = np.ravel(img)
    print(f'Image size (pixels) before compression: {img.shape[0]}')
    from time import time
    start_time = time()
    res = d.encode(img)
    print(f'Compression has taken {time() - start_time}')
    start_time = time()
    res = d.decode(res)
    print(f'Decompression has taken {time() - start_time}')
    assert np.all(img == res)
