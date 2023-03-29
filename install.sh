#!/bin/bash

pip install virtualenv
virtualenv C:\Users\%USERNAME%\Pic2AnkiEnv --python=python3.8
C:\Users\%USERNAME%\Pic2AnkiEnv\Scripts\activate
pip install -r .\requirements.txt
