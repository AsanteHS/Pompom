#!/usr/bin/env bash
set -e
DIR=$(dirname "$0")
cd ${DIR}/..

echo "Running tests with py.test and coverage"
py.test --cov
echo "pytest OK :)"
