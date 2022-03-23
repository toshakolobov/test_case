#!/bin/bash

PYTHON_ROOT="$HOME/Miniconda3/bin"

VENV_NAME="venv"

#if [ -d $VENV_NAME ]; then
#    rm -rf $VENV_NAME
#fi

#pip install virtualenv
$PYTHON_ROOT/virtualenv $VENV_NAME
$VENV_NAME/bin/pip install -r requirements.txt
