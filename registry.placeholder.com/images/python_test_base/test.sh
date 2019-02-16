#! /usr/bin/env bash

set -eu -o pipefail

cd /python_test
pytest -xs $@
