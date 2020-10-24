# Test functions goes here
import unittest

from huffman import encode, decode

class TestHuffman(unittest.TestCase):
	# write all your tests here
	# function name should be prefixed with 'test'

	def test_encode(self):
		encode("test_file.txt", "test_file.huff")
		assert True

	def test_encode(self):
		encode("story.txt", "story.huff")
		assert True

	def test_decode(self):
		decode("test_file.huff", "test_file_.txt")
		assert True

	def test_decode(self):
		decode("story.huff", "story_.txt")
		assert True


if __name__ == '__main__':
	unittest.main()
