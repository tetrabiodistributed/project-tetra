#!/bin/sh

if ! [ -d venv ]; then
    python3 -m venv venv
    source ./venv/bin/activate
    if [ -r requirements.txt ]; then
        pip3 install -r requirements.txt
    fi
fi

echo run this:
echo source ./venv/bin/activate
