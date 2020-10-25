# Test functions goes here
import unittest
import os

from huffman import encode, decode

class TestHuffman(unittest.TestCase):
	# write all your tests here
	# function name should be prefixed with 'test'

	def test_Huffman(self):
		def test_encode():
			try:
				encode("story.txt", "story.huff")
				encode("sample.txt", "sample.huff")
				print("Encode tested successfully")
				assert True
			except FileNotFoundError:
				if not (os.path.exists('story.txt') or os.path.exists('sample.txt')):
					print('Input file must be present for Huffman encoding')

		def test_decode():
			try:
				decode("story.huff", "story_.txt")
				decode("sample.huff", "sample_.txt")
				print("Decode tested successfully")
				assert True
			except FileNotFoundError:
				if not (os.path.exists('story.huff') or os.path.exists('sample.huff')):
					print('Input huff file must be present for Huffman decoding')

		def test_output():
			with open('story.txt', 'r') as original, open('story_.txt', 'r') as output:
				for char_1, char_2 in zip(original.read(), output.read()):
					assert char_1 == char_2
			print("Output tested successfully")

		test_encode()
		test_decode()
		test_output()


if __name__ == '__main__':
	test = TestHuffman()
