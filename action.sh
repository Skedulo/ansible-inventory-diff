#!/bin/bash
set -eux

function escape_whitespace {
  local result="$1"
  result="${result//'%'/'%25'}"
  result="${result//$'\n'/'%0A'}"
  result="${result//$'\r'/'%0D'}"
  echo "$result"
}

result="$(/bin/ansible-inventory-diff.sh --dir /github/workspace $1)"

maxlength=$2
length=$(echo "$result" | wc -l | awk '{print $1}')
if [ $length -gt $maxlength ] ; then
  snippet=$(echo "$result" | head -$maxlength)
  omitted=$(($length - $maxlength))
  snippet=$(escape_whitespace "$snippet")
  echo "::set-result name=snippet::${snippet}%0A...${omitted} lines omitted"
  result=$(escape_whitespace "$result")
else
  snippet=$(escape_whitespace "$result")
  echo "::set-result name=snippet::${snippet}"
  result=$(escape_whitespace "$result")
fi

echo "::set-result name=result::$result"
