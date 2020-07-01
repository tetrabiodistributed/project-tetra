#!/bin/sh

if ! [ -d venv ]; then
    python3 -m venv venv
fi


source ./venv/bin/activate

if [ -f requirements.txt ]; then
    pip3 install -r requirements.txt
fi

deactivate

if ! command -v docker &> /dev/null; then
    echo $'\nPlease install Docker'
fi

echo $'\nRun this to start the virtual environment'
echo source ./venv/bin/activate
