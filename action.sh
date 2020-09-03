#!/bin/bash
set -eu

echo "::set-output name=result::"$(/bin/ansible-inventory-diff.sh "$@")
