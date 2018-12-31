#!/usr/bin/env bash

. ~/.bashrc

python3 -m venv .python-env

. ./.python-env/bin/activate

if [[ ! -f ./.python-env/bin/conan ]]; then
    pip install conan
fi

export CONAN_USER_HOME="$(pwd)"

conan config install ./.conan-config
