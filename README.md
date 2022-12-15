# Huffman Encoding

A basic text file compression algorithm in Python3. Introduce [parallel processing](https://stackoverflow.com/questions/31796662/is-there-any-way-to-parallelize-huffman-encoding-implementation-on-hardware) to speedup the processing of large files.
This is an **individual assignment**. 
Write your solution and do not work in a pair/group on this program.

## Inputs
```
# To compress a file
huffman.py -e story.txt -o story.huff
# To extract a file
huffman.py -d story.huff -o story_.txt
```

* Options
  * -e :  followed by the text file to compress.
  * -d :  followed by the compressed file to extract.
  * -o :  followed by the filename to write the content.

## Encode / Decode

* Encode the input file with the algorithm and write the encoded data to the file along with all the information, to decompress a file. Possibly one can maintain a header section to save all the encoding information. The encoded file can have an extension `*.huff`.

* Read the encoding section to get the information required to decode the file and write the decoded data to the file. The decoded file should be the same as the input file.

* Make use of the script `diff.sh` which gives the detailed differences between the input and the decoded file, which can be helpful in the long run (one can avoid manual inspections) and gives the idea about loss of data.

  ```bash
  ./diff.sh <INPUT_FILE> <DECODED_FILE>
  ```

* Create at least 3 tests (covering basic/edge cases) inside the test script to test all functions or modules.

## Evaluation

The code will be evaluated based on the design, readability, performance and accuracy. 
Submit Pull Request for evaluation. If you have any doubts, create an issue in the repo, so that others can also refer to it. Watch the recorded session in case if you have missed it.

## Guidelines

Before submitting PR, make sure you run the below scripts. These scripts run all the test and evaluate your code.

```bash
# run all the tests in test.py
./run_test.sh
# evaluate your code
./run.sh
```

## References

Follow the below references completely.

* [Standford assignment on Huffman](https://web.stanford.edu/class/archive/cs/cs106b/cs106b.1178/assn/huffman.pdf)
* [How to send PR](https://www.freecodecamp.org/news/how-to-make-your-first-pull-request-on-github-3/)
* [How to write perfect PR](https://github.blog/2015-01-21-how-to-write-the-perfect-pull-request/)
