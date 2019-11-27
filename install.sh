#!/bin/bash

clear

git pull

# GET SCRIPT PATHS #
SCRIPT_PATH="$( cd "$(dirname "$0")" ; pwd -P )"
cd ${SCRIPT_PATH}

PROJECT_PATH=$PWD
ENVIRONMENTS_FOLDER=${PROJECT_PATH}
ENVIRONMENT="venv"

# INSTALL ENVIRONMENT #
echo -e "Installing requirements..."

cd ${PROJECT_PATH}

[[ -d ${ENVIRONMENTS_FOLDER} ]] || mkdir ${ENVIRONMENTS_FOLDER}
cd ${ENVIRONMENTS_FOLDER}

echo -e "Creating environment $ENVIRONMENT...\n\n"
python3 -m virtualenv ${ENVIRONMENT}

echo -e "Activating environment $ENVIRONMENT...\n\n"
source ${ENVIRONMENTS_FOLDER}/${ENVIRONMENT}/bin/activate

# INSTALL REQUIREMENTS #
echo -e "Installing requirements...\n"
pip3 install -r ${PROJECT_PATH}/requirements.txt | grep -v 'already satisfied'

echo -e "Done."