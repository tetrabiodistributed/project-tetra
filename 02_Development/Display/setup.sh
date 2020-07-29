#!/bin/sh

HIGHLIGHT='\033[0;33m'
NO_COLOR='\033[0m'


if ! [ -d venv ]; then
    python3 -m venv venv
fi

. venv/bin/activate

if [ -f requirements.txt ]; then
    pip3 install -r requirements.txt
fi

deactivate

if ! command -v docker &> /dev/null; then
    printf "\n${HIGHLIGHT}Please install Docker${NO_COLOR}"
fi

echo $'\nRun this to start the virtual environment'
printf "${HIGHLIGHT}. venv/bin/activate${NO_COLOR}\n"
