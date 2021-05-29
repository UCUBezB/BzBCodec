import heapq
import numpy as np
from collections import Counter, namedtuple


class Node():
    '''
    Class for creating Nodes and moving through them.

    Attributes
    ----------
    left:        left child
    right:        right child

    Methods
    -------
    move()
    '''
    def __init__(self, left, right) -> None:
        """[Initializes variables for Node]
        """
        self.left = left
        self.right = right

    def move(self, text, prefix):
        """[Moving through Node]
        """
        self.left.move(text, prefix + '0')
        self.right.move(text, prefix + '1')


class Leaf():
    '''
    Class for creating Nodes and moving through them.

    Attributes
    ----------
    symbol:        symbol that will be coded

    Methods
    -------
    move()
    '''
    def __init__(self, symbol) -> None:
        """[Initializes variables for Leaf]
        """
        self.symbol = symbol
    def move(self, text, prefix):
        """[Moves through the tree]
        """
        if not prefix:
            prefix = '0'
        text[self.symbol] = prefix


class HuffmanCode():
    '''
    Class for encoding and decoding numpy array with HuffmanCode.

    Attributes
    ----------
    data:        information about file

    Methods
    -------
    encode()
    decode()
    '''

    def __init__(self, data):
        """[Initializes variables for HuffmanCode]

        Args:
            data: [information about file]
        """        
        self.data = data

    def encode(self):
        """[Encodes numpy array with HuffmanCode]
        """
        tree = []
        coded_text = {}
        count = Counter(self.data)

        for symbol, frequency in count.items():
            tree.append((frequency, len(tree), Leaf(symbol)))

        heapq.heapify(tree)
        indicator = len(tree)

        while len(tree) > 1:
            first_frequency, _, left = heapq.heappop(tree)
            second_frequency, _, right = heapq.heappop(tree)
            heapq.heappush(tree, (first_frequency + second_frequency, indicator, Node(left, right)))
            indicator += 1

        if tree:
            [(_, _, root)] = tree
            root.move(coded_text, '')

        encoded = ''
        for symbol in self.data:
            encoded += str(coded_text[symbol])
        return encoded, coded_text

    def decode (self, decode_dict):
        """[Decodes coded text with HuffmanCode]
        """
        res = []
        while self.data:
            for key in decode_dict.keys():
                if self.data.startswith(decode_dict[key]):
                    self.data = self.data[len(decode_dict[key]):]
                    res.append(key)
        return res

if __name__ == '__main__':
    a = HuffmanCode(np.array([-1,2,1,-3,-1,2,1,-1,-1,0,1,1,-1,-1,2,1,-3,-1,3,0,-2,1,1,-1,
 0,0,0,1,0,-1,-1,0,1,1,0,-2,-1,3,2,-4,-3,5,3,-6,-2,6,0,-5,
 1,4,-2,-3,3,3,-3,-4,2,4,-1,-3,0,2,0,0,0,-2,0,3,0,-4,0,4,
 0,-3,0,2,0,-1,0,0,0,0,0,0,1,0,-2,0,3,0,-3,0,2,0,-2,0,
 2,0,-1,-1,1,3,-1,-5,0,6,0,-5,0,3,1,-2,-1,2,1,-3,-2,4,2,-4,
-1,3,0,-1,1,-1,-2,1,2,-1,-1,2,0,-2,0,2,0,-2,0,1,0,0,1,0,
-1,0,-1,1,3,-2,-4,2,4,-2,-3,1,2,1,-2,-2,2,2,-2,-2,2,2,-1,-2,
 0,3,0,-4,0,4,1,-3,-2,2,2,-1,-1,0,0,1,1,-2,-2,3,2,-3,-1,3,
 0,-3,0,2,0,-1,0,0]))
    b, coded_text = a.encode()
    print(b)
    print()
    c = HuffmanCode(b)
    print(c.decode(coded_text))
