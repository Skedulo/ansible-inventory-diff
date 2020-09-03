#!/bin/bash
set -eu

echo "::set-output name=result::"$(./ansible-inventory-diff "$@")
