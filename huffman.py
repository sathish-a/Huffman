#!/usr/local/bin/python3
import sys
import argparse
import shutil
from collections import Counter
import operator
import codecs
import pickle

class Node:
	"""
	This class is defined for the structure of the node in the Huffman tree.
	....
	Attributes
	----------
	char : unique character
	key : frequency of the character
	left : holds the left node of type Node
	right : holds the right node of type Node
	"""
	def __init__(self, char, key, left_node=None, right_node=None):
		self.char = char
		self.key = key
		self.left = left_node
		self.right = right_node

class Huffman:
	"""
	This class contains all the inbuilt functionalities required to encode or decode the given file.
	...
	Attributes
	----------
	root : Holds the root node of the Huffman tree
	queue : Holds the list of tuples containing unique characters and their frequencies
	nodeList : Holds the list of nodes required for the Huffman tree
	codes : Dict consisting the unique character as key and corresponding Huffman code as value
	reverse_mapping : Dict consisting the Huffman code as key and the corresponding character as value
	"""
	def __init__(self):
		self.root = None
		self.queue = []
		self.nodeList = []
		self.codes = {}
		self.reverse_mapping = {}


	def get_character_frequency(self, contents):
		"""
		Creates a queue of tuple elements containing the unique character and it's frequency in the input file
		"""
		frequency = dict(Counter(contents))
		self.queue = sorted(frequency.items(), key=operator.itemgetter(1))
		return self.queue


	def make_node_list(self):
		"""
		Creates a list containing nodes 
		"""
		while len(self.queue) > 0:
			a = self.queue.pop(0)
			newNode = Node(a[0], a[1])
			self.nodeList.append(newNode)


	def insert_node(self, inode):
		"""
		Inserts the new node to the list and sorts it
		"""
		for i, node in enumerate(self.nodeList):
			if inode.key >= node.key:
				self.nodeList.insert(i, inode)
				return


	def build_huffman_tree(self):
		"""
		Creates a Huffman tree
		"""
		self.make_node_list()
		if len(self.nodeList) == 1:
			self.root = self.nodeList[0]
			return
		while True:
			l = self.nodeList.pop(0)
			r = self.nodeList.pop(0)
			newNode = Node(None, l.key + r.key, l, r)
			self.insert_node(newNode)
			if len(self.nodeList) == 2:
				break
		l = self.nodeList.pop(0)
		r = self.nodeList.pop(0)
		newNode = Node(None, l.key + r.key, l, r)
		self.root = newNode


	def make_codes(self, root, current_code):
		"""
		Maps the character to the Huffman code
		"""
		if(root == None):
			return
		
		if(root.char != None):
			if len(self.nodeList) == 1:
				self.codes[root.char] = '0'
				self.reverse_mapping['0'] = root.char
			else:
				self.codes[root.char] = current_code
				self.reverse_mapping[current_code] = root.char
			return

		self.make_codes(root.left, current_code + '0')
		self.make_codes(root.right, current_code + '1')


	def make_codes_dict(self):
		"""
		Creates a dict of character and huffman codes
		"""
		self.make_codes(self.root, '')
		with open('_code.pkl'.format(),'wb') as f:
			pickle.dump(self.codes,f)
		f.close()
		with open('_rev_code.pkl','wb') as f:
			pickle.dump(self.reverse_mapping,f)
		f.close()


	def get_encoded_bytes(self, text):
		"""
		Encodes the text to bits
		"""
		q = self.get_character_frequency(text)
		self.build_huffman_tree()
		self.make_codes_dict()
		encoded_text = ''
		for character in text:
			encoded_text += self.codes[character]
		return encoded_text
	
	
	def get_decoded_text(self, encoded_text):
		"""
		Decodes the bits to character
		"""
		current_code = ""
		decoded_text = ""
		with open('_rev_code.pkl', 'rb') as f: 
			self.reverse_mapping = pickle.load(f)
		f.close()
		for bit in encoded_text:
			current_code += bit
			if(current_code in self.reverse_mapping):
				character = self.reverse_mapping[current_code]
				decoded_text += character
				current_code = ""
		return decoded_text



def encode(input_file, output_file):
	print("encoding ", input_file, output_file)
	huffman = Huffman()
	# Read the input txt file to be encoded
	with open(input_file, 'r+') as file:
		text_contents = file.read()
	file.close()

	# Obtain the encoded bytes from the input text
	encoded_text = huffman.get_encoded_bytes(text_contents)
	
	# Write the encoded bytes to the output file
	with open(output_file, 'w', encoding='utf-8') as write_file:
		write_file.write(encoded_text)
	write_file.close()


def decode(input_file, output_file):
	print("decoding ", input_file, output_file)
	huffman = Huffman()

	# Read the encoded input file
	with open(input_file, 'r', encoding='utf-8') as file:
		encoded_bytes = file.read()
	file.close()
	
	# Obtain the decoded text from the encoded bytes
	decoded_text = huffman.get_decoded_text(encoded_bytes)
	
	# Write the decoded text to output file
	with open(output_file, 'w') as write_file:
		write_file.write(decoded_text)
	write_file.close()


def get_options(args=sys.argv[1:]):
	parser = argparse.ArgumentParser(description="Huffman compression.")
	groups = parser.add_mutually_exclusive_group(required=True)
	groups.add_argument("-e", type=str, help="Encode files")
	groups.add_argument("-d", type=str, help="Decode files")
	parser.add_argument("-o", type=str, help="Write encoded/decoded file", required=True)
	options = parser.parse_args()
	return options


if __name__ == "__main__":
	options = get_options()
	if options.e is not None:
		encode(options.e, options.o)
	if options.d is not None:
		decode(options.d, options.o)
