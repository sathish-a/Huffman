#!/bin/bash
echo "diff of $1 and $2"
{ wc $1 && wc $2; } | awk 'NR==1 {line=$1; word=$2; char=$3; next} {line-=$1; word-=$2; char-=$3} END {printf "lines: %d\nwords: %d\nchars: %d\n", line, word, char; if(line+word+char != 0) exit 1 }'
