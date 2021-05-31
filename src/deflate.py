'''
!!! TODO: THOUGH IT SHOWS THAT MORE CHARACTERS ARE USED, THEY ARE ONLY 0 AND 1S,
IN COMPARISSON WITH OTHER ALGOS (WHERE DIFFERENT NUMES ARE WRITTEN)
'''

import numpy as np
from typing import Dict
from lz77 import compress, decompress
from Huffman_algo import HuffmanCode

class Deflate:
    '''
    Simple realisation of Deflate coding algorithm, which is based on
    LZ77 and Huffman compression algos.
    '''

    def encode(self, data: np.array) -> np.array:
        '''
        Encodes the data using LZ77 and Huffman codding

        TODO: because of bytes usage, max_length of offset is only 256. Because of this,
        it would work bas for pictures where are a lot of repetition (?????).
        '''

        # usage of lz77's method compress
        codewords = compress(data, max_length=255)

        codewords_bytes = bytes()
        for codeword in codewords:
            codewords_bytes += bytes([codeword[0]]) # codeword offset
            codewords_bytes += bytes([codeword[1]]) # codeword length
            codewords_bytes += bytes([codeword[2]]) # codeword char

        encoded_data, codes_table = HuffmanCode(codewords_bytes).encode()

        return encoded_data, codes_table
    

    def decode(self, compressed_data: np.array, codes_table: Dict[int, str]) -> np.array:
        '''
        Decodes the message, using the decode-implementation of LZ77 and Huffman.

        Takes: compressed data in np.array([List[int]]) format.
        '''

        decoded_huffman = HuffmanCode(compressed_data).decode(codes_table)
        data_to_decompress = [decoded_huffman[n:n+3] for n\
                             in range(0, len(decoded_huffman), 3)]
        data = decompress(data_to_decompress)
        
        return np.array([int(elm) for elm in data])
    

if __name__ == '__main__':
    d = Deflate()
    # -------- text usage example -----------
    msg = np.array([ord(elm) for elm in 'TOBEORNOTTOBEORTOBEORNOT'])
    print(f'Initial message: {msg}. Its lenght is: {len(msg)}')
    d = Deflate()
    compressed, codes_table = d.encode(msg)
    print(f'Length of compressed message is {len(compressed)}')

    res = d.decode(compressed, codes_table)
    print(f'Message after coding and decoding: {res}')
    assert list(msg) == list(res)

    # -------- image usage example ----------
    print()
    from PIL import Image
    img = Image.open('examples/test_img_3.png').convert('RGB')
    img = np.array(img.getdata())
    img = np.ravel(img)
    print(f'Image size (pixels) before compression: {img.shape[0]}')
    from time import time
    start_time = time()
    compressed, codes_table = d.encode(img)
    print(f'Length after compression: {len(compressed)}')
    print(f'Compression has taken {time() - start_time}')
    start_time = time()
    res = d.decode(compressed, codes_table)
    print(f'Decompression has taken {time() - start_time}')
    assert list(img) == list(res)
