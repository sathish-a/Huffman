#!/usr/bin/env bash
# encode story.txt
time python3 huffman.py -e story.txt -o story.huff
# decode story.txt
time python3 huffman.py -d story.huff -o story_.txt
# find differences
./diff.sh story.txt story_.txt
#find compression ratio
echo "Compression ratio"
expr $(ls -l story.txt | awk '{ print $5 }')/$(ls -l story.huff | awk '{ print $5 }') | bc -l
