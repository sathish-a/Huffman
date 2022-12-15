# Test functions goes here
import unittest

from huffman import encode, decode

class TestHuffman(unittest.TestCase):
	# write all your tests here
	# function name should be prefixed with 'test'

	def test_encode(self):
		encode("", "")
		assert True

	def test_decode(self):
		decode("", "")
		assert True


if __name__ == '__main__':
	unittest.main()
