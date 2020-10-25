#!/usr/local/bin/python3
import argparse
import heapq
import os
import pickle
import sys
from collections import defaultdict


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        if(other == None):
            return False
        if(not isinstance(other, Node)):
            return False
        return self.freq == other.freq


def encode(input_file, output_file):
    print("encoding ", input_file, output_file)
    # write code here

    bin_codes = {}
    with open(input_file, 'r+') as file, open(output_file, 'wb') as output:
        text = file.read()

        freq = defaultdict(int)
        heap_list = []

        for char in text:
            freq[char] += 1

        for char in sorted(freq):
            node = Node(char, freq[char])
            heapq.heappush(heap_list, node)

        while(len(heap_list) > 1):
            node1 = heapq.heappop(heap_list)
            node2 = heapq.heappop(heap_list)

            new_node = Node(None, node1.freq + node2.freq)
            new_node.left = node1
            new_node.right = node2

            heapq.heappush(heap_list, new_node)

        root = heapq.heappop(heap_list)
        code = ""

        def get_bin_codes(root, code):

            if(root == None):
                return

            if(root.char != None):
                bin_codes[root.char] = code
                return

            get_bin_codes(root.left, code + "0")
            get_bin_codes(root.right, code + "1")

        get_bin_codes(root, code)

        result = ""
        for char in text:
            result += bin_codes[char]

        padding = 8 - len(result) % 8
        for i in range(padding):
            result += "0"

        pad_info = "{0:08b}".format(padding)

        min_char = ''
        min_length = 100
        for key in bin_codes.keys():
            if len(bin_codes[key]) <= min_length:
                min_char = key

        pseudo_EOF = bin_codes[min_char] + '1'
        pseudo_EOF = pseudo_EOF.rjust(8, '0')
        temp_result = pad_info + pseudo_EOF

        map_str = ""
        for char in sorted(bin_codes.keys()):
            map_str = map_str + f'{ord(char):08b}'
        map_str += pseudo_EOF

        for char in sorted(bin_codes.keys()):
            map_str = map_str + bin(freq[char])[2:].rjust(16, '0')

        result = temp_result + map_str + result

        b = bytearray()
        for i in range(0, len(result), 8):
            byte = result[i:i+8]
            b.append(int(byte, 2))
        output.write(bytes(b))
        print("Compressed")


def decode(input_file, output_file):
    print("decoding ", input_file, output_file)
    # write code here

    bin_codes = {}
    heap_list = []

    with open(input_file, 'rb') as file, open(output_file, 'w') as output:

        bit_string = ""
        byte = file.read(1)
        while byte:
            bit_string += f'{ord(byte):08b}'
            byte = file.read(1)

        padding = int(bit_string[:8], 2)
        pseudo_EOF = bit_string[8:16]

        bit_string = bit_string[16:-1*padding]
        i = 16
        byte = ""
        char_array = []
        freq = {}
        while byte != pseudo_EOF:
            char_array.append(chr(int(bit_string[i:i+8], 2)))
            byte = bit_string[i:i+8]
            i += 8

        j = 0
        char_array = ['\n', ' '] + char_array
        char_array.remove('\x07')

        while j < len(char_array):
            freq[char_array[j]] = int(bit_string[i:i+16], 2)
            i += 16
            j += 1

        for char in sorted(freq):
            node = Node(char, freq[char])
            heapq.heappush(heap_list, node)

        while(len(heap_list) > 1):
            node1 = heapq.heappop(heap_list)
            node2 = heapq.heappop(heap_list)

            new_node = Node(None, node1.freq + node2.freq)
            new_node.left = node1
            new_node.right = node2

            heapq.heappush(heap_list, new_node)

        root = heapq.heappop(heap_list)
        code = ""

        def get_bin_codes(root, code):

            if(root == None):
                return

            if(root.char != None):
                bin_codes[root.char] = code
                return

            get_bin_codes(root.left, code + "0")
            get_bin_codes(root.right, code + "1")

        get_bin_codes(root, code)

        bin_codes = {v: k for k, v in bin_codes.items()}

        bit_string = bit_string[i:]
        code = ""
        result = ""
        for bit in bit_string:
            code += bit
            if(code in bin_codes):
                char = bin_codes[code]
                result += char
                code = ""

        output.write(result)
        print("Decompressed")


def get_options(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Huffman compression.")
    groups = parser.add_mutually_exclusive_group(required=True)
    groups.add_argument("-e", type=str, help="Encode files")
    groups.add_argument("-d", type=str, help="Decode files")
    parser.add_argument(
        "-o", type=str, help="Write encoded/decoded file", required=True)
    options = parser.parse_args()
    return options


if __name__ == "__main__":
    options = get_options()
    if options.e is not None:
        encode(options.e, options.o)
    if options.d is not None:
        decode(options.d, options.o)
