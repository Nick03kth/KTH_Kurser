import heapq
from collections import Counter, namedtuple

class HuffmanNode(namedtuple("Node", ["char", "freq", "left", "right"])):
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    frequency = Counter(text)
    if len(frequency) == 1:  # Specialfall: bara ett tecken
        char = next(iter(frequency))
        return HuffmanNode(char, frequency[char], None, None)
    heap = [HuffmanNode(char, freq, None, None) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        new_node = HuffmanNode(None, left.freq + right.freq, left, right)
        heapq.heappush(heap, new_node)

    return heap[0]

def huffman_codes(tree, prefix="", code_map=None):
    if code_map is None:
        code_map = {}
    if tree.char is not None:
        code_map[tree.char] = prefix or "0"  # Om bara ett tecken, använd "0" som kod
    else:
        huffman_codes(tree.left, prefix + "0", code_map)
        huffman_codes(tree.right, prefix + "1", code_map)
    return code_map

def huffman_encode(text):
    if not text:  # Specialfall: tom text
        return "", None
    tree = build_huffman_tree(text)
    codes = huffman_codes(tree)
    encoded_text = ''.join(codes[char] for char in text)
    return encoded_text, tree

def huffman_decode(encoded_text, tree):
    if tree.left is None and tree.right is None:  # Trivialt träd
        return tree.char * len(encoded_text)  # Returnera originaltexten
    result = []
    node = tree
    for bit in encoded_text:
        node = node.left if bit == "0" else node.right
        if node.char:
            result.append(node.char)
            node = tree
    return ''.join(result)
