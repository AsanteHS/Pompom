#!/bin/bash

set -e
DIR=$(dirname "$0")
cd ${DIR}/..

echo "Running pylint with py.test"
py.test --pylint
echo "pylint OK :)"
