#!/usr/bin/env bash
set -e
DIR=$(dirname "$0")
cd ${DIR}/..

echo "Running py.test with pep8, pylint and coverage"
py.test --cov --pep8 --pylint
echo "pytest OK :)"
