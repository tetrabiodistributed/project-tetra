#!/bin/sh

echo "Behaviour Tests:"
behave
echo $'\nUnit Tests:'
python3 -m unittest
