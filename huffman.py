#!/usr/local/bin/python3
import sys
import argparse
import shutil

import os
from collections import Counter
from queue import PriorityQueue

class HuffmanNode:

    def __init__(self, char, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCompressor:
    
    def __init__(self):

        self.frequencies = ""
        self.huffman_tree = []
        self.code_table = {}
        self.encoded_text_code = ""
        self.encoded_tree_code = ""

    def encode(self, input_file, output_file):

        print("\nEncoding ", input_file, output_file)
        
        with open(input_file) as in_file, open(output_file, "wb") as out_file:
            text = in_file.read()
            
            # 1. Generate Tree and Append Frequencies to Queue
            
            self.huffman_tree = self.generate_tree(text)
            
            # 2. Produce Code table with code
            self.add_code_table(self.huffman_tree, "", self.code_table)

            
            for c in text:
                self.encoded_text_code += self.code_table[c]
            
            # 3. Convert to binary
            self.encoded_tree_code = self.bin_encode(self.huffman_tree, "")

            # 4. Adding prefix 0's 
            bits = self.add_prefix_zeros()

            encoded_text = f"{self.encoded_tree_code}{bits:08b}{self.encoded_text_code}"

            # 5. Writing bytearray to output file
            b_arr = bytearray()
            for i in range(0, len(encoded_text), 8):
                b_arr.append(int(encoded_text[i:i+8], 2))

            out_file.write(b_arr)

            # Printing compression ratio
            self.print_ratio(input_file,output_file)



    def decode(self,input_file, output_file):
            
        print("Decoding ", input_file, output_file)

        with open(input_file, "rb") as in_file, open(output_file, "w",  encoding='utf-8') as out_file:
            encoded_text = ""

            byte = in_file.read(1)
            while len(byte) > 0:
                encoded_text += f"{bin(ord(byte))[2:]:0>8}"
                byte = in_file.read(1)

            encoded_text_ar = list(encoded_text)
            encoded_tree = self.bin_decode(encoded_text_ar)

            # 1. Remove extra zeros
            self.remove_prefix_zeros(encoded_text_ar)

            # 2. Decode text
            text = ""
            current_node = encoded_tree
            for char in encoded_text_ar:
                current_node = current_node.left if char == '0' else current_node.right

                if current_node.char is not None:
                    text += current_node.char
                    current_node = encoded_tree

            # 3. Writing decoded text
            out_file.write(text)

    def generate_tree(self,text):

        self.frequencies = Counter(text)
        queue = PriorityQueue()
        

        for char, f in self.frequencies.items():
            queue.put(HuffmanNode(char, f))

        # Merge nodes
        while queue.qsize() > 1:
            l, r = queue.get(), queue.get()
            queue.put(HuffmanNode(None, l.freq + r.freq, l, r))

        huffman_tree = queue.get()

        return huffman_tree

    def add_code_table(self, node, code, code_table):
        """Fill code table, which has chars and corresponded codes"""

        if node.char is not None:
            code_table[node.char] = code
        else:
            self.add_code_table(node.left, code + "0", code_table)
            self.add_code_table(node.right, code + "1", code_table)

    def bin_encode(self, node, tree_text):
        """ Encode huffman tree in binary to save it in the file """

        if node.char is not None:
            tree_text += "1"
            tree_text += f"{ord(node.char):08b}"
        else:
            tree_text += "0"
            tree_text = self.bin_encode(node.left, tree_text)
            tree_text = self.bin_encode(node.right, tree_text)

        return tree_text

    def bin_decode(self, tree_code_ar):
        """ Decoding huffman tree to be able to decode the encoded text"""
    
        code_bit = tree_code_ar[0]
        del tree_code_ar[0]

        if code_bit == "1":
            char = ""
            for _ in range(8):
                char += tree_code_ar[0]
                del tree_code_ar[0]

            return HuffmanNode(chr(int(char, 2)))

        return HuffmanNode(None, left=self.bin_decode(tree_code_ar), right=self.bin_decode(tree_code_ar))
    
    def add_prefix_zeros(self):

        number = 8 - (len(self.encoded_text_code) + len(self.encoded_tree_code)) % 8
        if number != 0:
            self.encoded_text_code = number * "0" + self.encoded_text_code

        return number

    def remove_prefix_zeros(self,encoded_text_ar):
        number_of_extra_0_bin = encoded_text_ar[:8]
        encoded_text_ar = encoded_text_ar[8:]
        number_of_extra_0 = int("".join(number_of_extra_0_bin), 2)
        encoded_text_ar = encoded_text_ar[number_of_extra_0:]          

    def print_ratio(self, input_path, output_path):
        before_size = os.path.getsize(input_path)
        after_size = os.path.getsize(output_path)
        compression_percent = round(100 - after_size / before_size * 100, 1)
        print(f"Before: {before_size}bytes, After: {after_size}bytes, "
            f"compression {compression_percent}%")


def get_options(args=sys.argv[1:]):

    parser = argparse.ArgumentParser(description="Huffman compression.")
    groups = parser.add_mutually_exclusive_group(required=True)
    groups.add_argument("-e", type=str, help="Encode files")
    groups.add_argument("-d", type=str, help="Decode files")
    parser.add_argument("-o", type=str, help="Write encoded/decoded file", required=True)
    args = parser.parse_args()
    
    return args


if __name__ == "__main__":

    args = get_options()
    compressor = HuffmanCompressor()

    if args.e is not None:
        compressor.encode(args.e, args.o)
    if args.d is not None:
        compressor.decode(args.d, args.o)
