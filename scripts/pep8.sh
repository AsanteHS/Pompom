#!/bin/bash

set -e
DIR=$(dirname "$0")
cd ${DIR}/..


echo "Running pep8 with py.test"
py.test --pep8

echo "pep8 OK :)"
