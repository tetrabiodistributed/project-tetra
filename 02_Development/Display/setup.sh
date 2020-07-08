#!/bin/sh

if ! [ -d venv ]; then
    python3 -m venv venv
fi

<<<<<<< HEAD
source ./venv/bin/activate

=======
>>>>>>> changed the sensors module so it will read data from a file when it's not run on a raspberry pi and added the start of a behave test to verify that the Docker image works.
if [ -f requirements.txt ]; then
    pip3 install -r requirements.txt
fi

<<<<<<< HEAD
deactivate

if ! command -v docker &> /dev/null; then
    echo $'\nPlease install Docker'
fi

echo $'\nRun this to start the virtual environment'
=======
echo $'\nrun this:'
>>>>>>> changed the sensors module so it will read data from a file when it's not run on a raspberry pi and added the start of a behave test to verify that the Docker image works.
echo source ./venv/bin/activate
