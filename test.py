# Test functions goes here
import unittest

from huffman import HuffmanCompressor
compressor =  HuffmanCompressor()

class TestHuffman(unittest.TestCase):
    
    # write all your tests here
    # function name should be prefixed with 'test'

    def test_encode(self):
        compressor.encode("story.txt", "story.huff")
        assert True

    def test_decode(self):
        compressor.decode("story.huff", "story.txt")
        assert True
    
    def test_generate_tree(self):
        text = "But for the past few days he had spoken to them about only one thing: the girl, the daughter of a merchant who lived in the village they would reach in about four days."
        compressor.generate_tree(text)
        assert True


if __name__ == '__main__':
    unittest.main()
