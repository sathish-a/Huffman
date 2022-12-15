#!/usr/bin/env bash
# profile encode
echo "Encoding"
sudo perf stat -e cycles,instructions,cache-references,cache-misses,branches,branch-misses,task-clock,faults,minor-faults,cs,migrations python3 huffman.py -e story.txt -o story.huff
# profile decode
echo "Decoding"
sudo perf stat -e cycles,instructions,cache-references,cache-misses,branches,branch-misses,task-clock,faults,minor-faults,cs,migrations python3 huffman.py -d story.huff -o story_.txt
