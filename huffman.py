#!/usr/local/bin/python3
import sys
import argparse
import shutil
# from collections import defaultdict
import heapq

class HeapNode:
	# Heap node class which contains left, right along with the char and frequency
	def __init__(self, character, frequency):
		self.char = character
		self.freq = frequency
		self.left = None
		self.right = None
	
	def __lt__(self, other):
		if other == None:
			return False
		return self.freq < other.freq

	def __eq__(self, other):
		if (other == None):
			return False
		if(not isinstance(other, HeapNode)):
			return False
		return self.freq == other.freq


def make_frequency(text):
	# creates a frequecy of the character in the string
	frequency = {}
	for character in text:
		if character not in frequency.keys():
			frequency[character] = 0
		frequency[character] += 1
	
	return frequency

def create_heap(frequency):
	# create min heap using heapq returns the heap list
	heap = []
	for character in frequency.keys():
		node = HeapNode(character, frequency[character])
		heapq.heappush( heap, node)
	return heap

def get_code( root, code, current_code):
	## gets the code for particular character
	if root.char != None:
		code[root.char] = current_code
		return code
	
	code = get_code(root.left, code, current_code+"0")
	code = get_code(root.right, code, current_code+"1")
	return code

def generate_code(heap):
	# creates code first by merging the heap and then generates and returns code
	while( len(heap) > 1):
		node1 = heapq.heappop(heap)
		node2 = heapq.heappop(heap)

		merge = HeapNode(None, node1.freq + node2.freq )
		merge.left = node1
		merge.right = node2
		heapq.heappush(heap, merge)

	root = heapq.heappop(heap)
	current_code = ""
	code = {}
	code = get_code(root, code, current_code)
	return code

def get_encoded_code(code):
	# convert the code dictionary to a binary format and stores the count of unique character
	encoded_code = ""
	count = 0
	for character in code.keys():
		x = "{0:08b}".format(ord(character))
		encoded_code += x
		# print("Character:",character,x,end = "\t")

		length = len(code[character])
		x = "{0:08b}".format(length)
		encoded_code += x
		# print("Length:",length,x,end = "\t")
		
		x = code[character]
		encoded_code += x
		count += 1
		# print("Code:",x, "\t",count)
	
	padded_code = "{0:08b}".format(count)
	encoded_code = padded_code + encoded_code
	return encoded_code

def get_encoded_text(code, text):
	# converts text to encoded format and inserts code information in front of the coded text
	encoded_text = ""
	for character in text:
		encoded_text += code[character]
	
	encoded_code = get_encoded_code(code)
	encoded_text = encoded_code + encoded_text
	return encoded_text

def get_padding(encoded_text):
	# if required pads the encoded text with zeros and return the padded text
	pad_count = 8 - len(encoded_text)%8

	for i in range(pad_count):
		encoded_text += "0"
	
	padding_info = "{0:08b}".format(pad_count)
	padded_text = padding_info + encoded_text
	return padded_text

def get_byte_array(padded_text):
	# converts the binary information into the byte information
	if len(padded_text)%8 != 0:
		print("ERROR: Encoded Data length is not a multiple of 8 to convert into byte")
	
	b = bytearray()

	for i in range(0,len(padded_text),8):
		byte = padded_text[i:i+8]
		byte = int(byte,2)
		b.append(byte)
	
	return b

def encode(input_file, output_file):
	print("encoding ", input_file, output_file)

	with open(input_file,'r') as input_f, open(output_file,'wb') as output:
		text = input_f.read()
		# text = text. ##removes unwanted ending spaces

		frequency = make_frequency(text)
		heap = create_heap(frequency)
		code = generate_code(heap)
		encoded_text = get_encoded_text(code , text)
		padded_text = get_padding(encoded_text)
		byte_text = get_byte_array(padded_text)
		output.write(bytes(byte_text) )

def remove_padding(bit_string):
	# removes the extra padding from the end
	padded_info = bit_string[:8]
	bit_string = bit_string[8:]
	# print(padded_info)
	padded_count = int(padded_info,2)
	bit_string = bit_string[:(-padded_count)]
	return bit_string

def get_reverse_codes(bit_string):
	# gets reverse codes from the encoded text
	reverse_code = {}
	count = bit_string[:8]
	bit_string = bit_string[8:]
	count = int(count,2)
	for i in range(count):
		a = bit_string[:8]
		character = chr(int(a,2))
		bit_string = bit_string[8:]
		# print("Character:",character,a,end = "\t")


		b = bit_string[:8]
		length = int(b,2)
		bit_string = bit_string[8:]
		# print("Length:",length,b,end = "\t")


		code = bit_string[:length]
		bit_string = bit_string[length:]
		reverse_code[code] = character
		# print("Code:",code, "\t",i)

	return reverse_code,bit_string

def get_decoded_text(reverse_code, encoded_text):
	# get decoded text using reverse code
	decoded_text = ""
	current_code = ""
	for bit in encoded_text:
		current_code += bit
		if current_code in reverse_code.keys():
			decoded_text += reverse_code[current_code]
			current_code = ""
	
	return decoded_text


def decode(input_file, output_file):
	print("decoding ", input_file, output_file)

	with open(input_file,'rb') as input_f, open(output_file,'w') as output:
		bit_string = ""
		byte = input_f.read(1)
		while( len(byte) > 0):
			byte = ord(byte)
			bits = bin(byte)[2:].rjust(8,"0")
			bit_string += bits
			byte = input_f.read(1)
		
		encoded_text = remove_padding(bit_string)
		reverse_code, encoded_text = get_reverse_codes(encoded_text)
		decoded_text = get_decoded_text(reverse_code, encoded_text)
		output.write(decoded_text)

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
