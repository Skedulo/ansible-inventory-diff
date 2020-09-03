#!/bin/bash
set -eu

result="$(/bin/ansible-inventory-diff.sh --dir /github/workspace $@)"
echo "$result"
result="${result//'%'/'%25'}"
result="${result//$'\n'/'%0A'}"
result="${result//$'\r'/'%0D'}"

echo "::set-output name=result::$result"
