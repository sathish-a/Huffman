#!/usr/local/bin/python3
import sys
import argparse
import shutil


def encode(input_file, output_file):
	print("encoding ", input_file, output_file)
	# write code here

	# simply copying the file to bypass the actual test.
	# remove the below lines.
	if input_file != "" and output_file != "":
		shutil.copyfile(input_file, output_file)


def decode(input_file, output_file):
	print("decoding ", input_file, output_file)
	# write code here

	# simply copying the file to bypass the actual test.
	# remove the below lines.
	if input_file != "" and output_file != "":
		shutil.copyfile(input_file, output_file)


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
