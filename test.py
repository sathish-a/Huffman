# Test functions goes here
import unittest

from huffman import encode, decode, Huffman

class TestHuffman(unittest.TestCase):
	# write all your tests here
	# function name should be prefixed with 'test'


	def test_encode(self):
		encode("story.txt", "story.huff")
		assert True

	def test_decode(self):
		decode("story.huff", "story_.txt") 
		assert True

	def test_get_character_frequency(self):
		queue = Huffman().get_character_frequency("Python -- easy")
		assert queue == [('P', 1), ('t', 1), ('h', 1), ('o', 1), ('n', 1), ('e', 1), ('a', 1), ('s', 1), ('y', 2), (' ', 2), ('-', 2)] 
		queue = Huffman().get_character_frequency("Sea shells sea shells\n On the sea shore")
		assert queue == [('S', 1), ('\n', 1), ('O', 1), ('n', 1), ('t', 1), ('o', 1), ('r', 1), ('a', 3), ('h', 4), ('l', 4), ('e', 7), (' ', 7), ('s', 7)]

	def test_encode_decode(self):
		encode_text = Huffman().get_encoded_bytes("\n")
		assert encode_text == "0"
		decode_text = Huffman().get_decoded_text("0")
		assert decode_text == "\n"
		encode_text = Huffman().get_encoded_bytes('"Huffman"')
		decode_text = Huffman().get_decoded_text(encode_text)
		assert decode_text == '"Huffman"'


if __name__ == '__main__':
	unittest.main()
