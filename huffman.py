#!/usr/local/bin/python3
import sys
import argparse
import shutil
from collections import OrderedDict

binary_code = { '\n' : "", '\t' : "", '/' : "", 'A' : "", 'B' : "", 'C' : "", 'D' : "", 'E' : "", 'F' : "", 'G' : "", 'H' : "", 'I' : "", 'J' : "", 'K' : "", 'L' : "", 'M' : "", 'N' : "", 'O' : "", 'P' : "", 'Q' : "", 'R' : "", 'S' : "", 'T' : "", 'U' : "", 'V' : "", 'W' : "", 'X' : "", 'Y' : "", 'Z' : "", 'a' : "", 'b' : "", 'c' : "", 'd' : "", 'e' : "", 'f' : "", 'g' : "", 'h' : "", 'i' : "", 'j' : "", 'k' : "", 'l' : "", 'm' : "", 'n' : "", 'o' : "", 'p' : "", 'q' : "", 'r' : "", 's' : "", 't' : "", 'u' : "", 'v' : "", 'w' : "", 'x' : "", 'y' : "", 'z' : "", '0' : "", '1' : "", '2' : "", '3' : "", '4' : "", '5' : "", '6' : "", '7' : "", '8' : "", '9' : "", '~' : "", '`' : "", '!' : "", '@' : "", '#' : "", '$' : "", '%' : "", '^' : "", '&' : "", '*' : "", '(' : "", ')' : "", '-' : "", '_' : "", '+' : "", '=' : "", '  ' : "", '[' : "", ']' : "", '{' : "", '}' : "", '\'': "", '<' : "", '>' : "", '\\' : "", '|' : "", '\"' : "", ';' : "", ':' : "", '.' : "", ',' : "", '?' : ""}

class Node:
	def __init__(self, char, count):
		self.left = None
		self.right = None
		self.char = char
		self.count = count
		self.isleaf = 1
		self.binary = ""
	def form(self,first,second):
		self.left = first
		self.right = second
		self.isleaf = 0

def set_binary(self):
	if self.left:
		self.left.binary = self.binary+'0'	#add 0 to binary on moving left
		if(self.left.isleaf):
			binary_code[self.left.char] = self.left.binary
		set_binary(self.left)
	if self.right:
		self.right.binary = self.binary+'1'	#	add 1 to binary on moving right
		if(self.right.isleaf):
			binary_code[self.right.char] = self.right.binary
		set_binary(self.right)

def binaryToChar(binary_string):
	n = int('0b'+binary_string, 2)
	c = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
	return c

def strToBytes(data):
	b = bytearray()
	for i in range(0, len(data), 8):
		b.append(int(data[i:i+8], 2))
	return bytes(b)

def get_frequency(input_file):
	frequency= {}
	with open(input_file) as f:
		for line in f:
			for word in line:
				if word in frequency.keys():
					frequency[word]=frequency[word]+1
				else:
					frequency[word] = 1
	return frequency

def get_priority_queue(frequency):
	priority_queue = []
	for i in frequency:
		if(frequency[i] > 0):
			n = Node(i,frequency[i])
			priority_queue.append(n) #Create nodes for all existing(count > 0) nodes to priority_queue
	return priority_queue

def form_tree(priority_queue):
	first = priority_queue.pop()
	second = priority_queue.pop()
	while 1:
		parent = Node(first.char+second.char, first.count+second.count)
		priority_queue.append(parent)	#add parent to priority_queue as well
		priority_queue.sort(key=lambda priority_queue: priority_queue.count, reverse=True)
		parent.form(first,second) #forms parent from first and second
		first = priority_queue.pop()
		if not priority_queue:	#breaks when only one node is left
			break
		second = priority_queue.pop()
	return first

def write_encode_info(binary_code,output_file):
	fs = open(output_file,'wb')
	count = 0
	for i in binary_code:
		if (binary_code[i] != ''):
			count += 1
	fs.write(count.to_bytes(1, 'little'))
	dot = '.'
	for i in binary_code:
		if (binary_code[i] != ''):
			fs.write(binary_code[i].encode())	#write encoded value of binary value
			fs.write(dot.encode())
			fs.write(i.encode())	#write encoded value of binary key
			fs.write(dot.encode())
	return fs

def append_encoded_content(fo,input_file,output_file,binary_code):
	fi = open(input_file,'r')
	input_file_content = fi.read()	#read the input text file
	input_encoded = ''.join([binary_code[literal] for literal in input_file_content])	#combine codes of all literals of file
	bit_count = len(input_encoded)	#nuumber of bits in encode
	mod8 = bit_count%8
	pad_length = 8 - mod8	#number of bits needed to make bit_count as multiple of 8
	if pad_length == 8:
			pad_length = 0
	zero_length = f'{bin(pad_length)[2:]:0>8}'	#binary representation of pad length
	pad_zeroes = '0' * pad_length	#replicate zeroes for padding
	input_encoded = input_encoded + pad_zeroes	#add padding to actual content
	input_encoded = zero_length + input_encoded		#add pad length to beginning of encoded_content
	fo.write(strToBytes(input_encoded))
	fo.close()

def get_decode_info(input_file):
	fi = open(input_file, 'rb')
	file_content = ''
	byte = fi.read(1)
	while len(byte) :
		file_content += f"{bin(ord(byte))[2:]:0>8}"
		byte = fi.read(1)
	margin = file_content[:8]	#first byte denotes the margin
	margin = int(margin, base=2)
	index = 8	#start after margin
	dot_count = 0
	break_point = 2*margin	#breakpoint refers the point to stop reading encoded info
	prev_dot = 0
	second_dot = 0	#previous and second dot are used to separate delimiter from actual dot 
	key = 1		#represents if next search (key or value)
	val = ''
	binary_decode = {}
	while 1:
		char = binaryToChar(file_content[index:(index+8)])
		index += 8
		if (char == '.'):
			dot_count += 1
			if(key == 1):	#reverses the search
				key = 0
			else:
				key = 1
			if(prev_dot == 1):	#special case of having dot as key 
				second_dot = 1
				key_ = '.'
				binary_decode[val] = key_
				val = ''
				key = 0
				prev_dot = 0
				second_dot = 0
			else:
				prev_dot = 1
			if (dot_count > break_point):
				break
		else:	#found key
			prev_dot = 0
			if(key == 0):
				key_ = char
				binary_decode[val] = key_
				val = ''
			else:	#append value till delimiter occurs
				val += char
	return index,binary_decode

def write_output(input_file,output_file,binary_decode,index):
	fi = open(input_file, 'rb')
	file_content = ''
	byte = fi.read(1)
	while len(byte) > 0:
		file_content += f"{bin(ord(byte))[2:]:0>8}"	#get input file content
		byte = fi.read(1)
	binary_pad = file_content[index:index+8]	#get zero pad length in first byte
	fo = open(output_file,'w+')
	input_data = file_content[(index+8):]	#store from next byte
	padded_val = int(binary_pad, base=2)
	if padded_val > 1:
		input_data = input_data[:-padded_val+1]	#remove the padded content
	start_ind = 0 	#start point of substring match
	end_ind = 1 	#end point of substring match
	len_ = len(input_data)
	decoded_content = ''
	while end_ind < len_:
		sub_str = input_data[start_ind:end_ind]
		if sub_str in binary_decode.keys():
			decoded_content += binary_decode[sub_str]
			start_ind = end_ind		#key found write the value to file and start reading from next byte
		end_ind += 1
	# writing decoded text to a text file
	fo.write(decoded_content)
	fo.close()

def encode(input_file, output_file):
	frequency = get_frequency(input_file)
	a = sorted(frequency.items(), key=lambda x: x[1])
	frequency =OrderedDict(a)
	priority_queue = get_priority_queue(frequency)
	priority_queue.reverse()
	root = form_tree(priority_queue)	#form tree from priority queue
	set_binary(root)	#set binary for all nodes in tree
	fs = write_encode_info(binary_code,output_file)
	append_encoded_content(fs,input_file,output_file,binary_code)

def decode(input_file, output_file):
	margin,binary_decode = get_decode_info(input_file)
	write_output(input_file,output_file,binary_decode,margin)

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
