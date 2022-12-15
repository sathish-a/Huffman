#!/usr/bin/env bash
# run all the tests inside test.py
if python3 -c "import pytest" &> /dev/null ; then
    pytest test.py
else
    python3 -m unittest test.py >& test.log &
    wait
    fgrep FAILED test.log
fi
