#!/bin/bash

set -e
DIR=$(dirname "$0")
cd ${DIR}/..


echo "Running pep8 and pylint with py.test"
py.test --pep8 --pylint

echo "pep8 OK :)"
