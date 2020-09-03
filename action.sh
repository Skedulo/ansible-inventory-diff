#!/bin/bash
set -eu

result="$(/bin/ansible-inventory-diff.sh --dir /github/workspace $@)"
echo "$result"
echo "::set-output name=result::$result"
