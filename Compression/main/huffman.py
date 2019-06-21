import base64


class MinHeapNode:
    def __init__(self, char="", freq=0):
        self.char = char
        self.freq = freq
        self._left = None
        self._right = None
        self._is_parent = False

    @property
    def is_parent(self):
        return self._is_parent

    @is_parent.setter
    def is_parent(self, value: bool):
        self._is_parent = value

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def __add__(self, other):
        parent = MinHeapNode("", self.freq + other.freq)
        parent._left = self
        parent._right = other
        parent.is_parent = True
        return parent

    def __repr__(self):
        if self.is_parent:
            return "({}, ({}, {}))".format(self.freq, self._left, self._right)
        else:
            return "({}, '{}')".format(self.freq, self.char)

    def __lt__(self, other: 'MinHeapNode'):
        return self.freq < other.freq

    def __eq__(self, other: 'MinHeapNode'):
        return self.freq > other.freq

    def __gt__(self, other: 'MinHeapNode'):
        return self.freq == other.freq


class HuffmanTree:
    def __init__(self, content: str):
        self.node_list = []
        self.code_list = {}
        self._frequency(content)
        self.node = None
        self._create_tree(self.node_list)
        self._get_codes(self.node)

    def _create_tree(self, nodes: list):
        if len(nodes) == 1:
            self.node = nodes[0]
            return
        new_node = nodes[0] + nodes[1]
        nodes = nodes[2:]
        nodes.append(new_node)
        nodes.sort()
        self._create_tree(nodes)

    def _get_codes(self, node: 'MinHeapNode', string=""):
        if node.is_parent:
            self._get_codes(node.left, string+"0")
            self._get_codes(node.right, string+"1")
        else:
            self.code_list[node.char] = string

    def _frequency(self, content: str):
        _freq_dict = {}
        for ch in content:
            _freq_dict[ch] = _freq_dict.get(ch, 0) + 1
        letters = _freq_dict.keys()
        for letter in letters:
            self.node_list.append(MinHeapNode(letter, _freq_dict[letter]))
        self.node_list.sort()


class Compressor:
    def __init__(self):
        self.tree = None
        self._output = ""

    @property
    def output(self):
        return self._output

    def encode(self, content: str):
        if self._output != "":
            return
        content += '\n'
        self.tree = HuffmanTree(content)
        for char in content:
            self._output += self.tree.code_list[char]

    def decode(self):
        text = ""
        node = self.tree.node
        for bit in self._output:
            if node.is_parent:
                if bit == "0":
                    node = node.left
                elif bit == "1":
                    node = node.right
                if not node.is_parent:
                    text += node.char
                    node = self.tree.node
            else:
                text += node.char
                node = self.tree.node
        return text[:-1]

    def compress(self):
        dat = ''.join(chr(int(self._output[i:i+8], 2)) for i in range(0, len(self._output), 8))
        return dat

if __name__ == "__main__":
    c = Compressor()
    c.encode("01010100001000010101000101010001010")
    print(c.tree.code_list)
    print(c.output)
    print(c.decode())
    print(c.compress())
    # try:
    #     file = open("compressed.txt", "w")
    #     file.write(txt)
    # finally:
    #     file.close()
