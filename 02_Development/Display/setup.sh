#!/bin/sh

if ! [ -d venv ]; then
    python3 -m venv venv
fi

if [ -f requirements.txt ]; then
    pip3 install -r requirements.txt
fi

echo $'\nrun this:'
echo source ./venv/bin/activate
