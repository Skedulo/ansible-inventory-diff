#!/bin/sh

set -eu

while [ $# -gt 0 ]; do
  case $1 in
    "-v")
      verbose="$1"
      ;;
    "--to")
      tocommit="$2"
      shift
      ;;
    *)
      if [ -z "${commit:-}" ] ; then
        commit="$1"
      else
        break
      fi
      ;;
  esac
  shift
done

if [ -z "${commit:-}" ] ; then
  echo "Usage: $0 [-v] <commitish> [group]"
  exit
fi

mkdir /src && cd /src
git clone -nqs /git a
git clone -nqs /git b

(cd a && git reset -q --hard "${commit}")
(cd b && git reset -q --hard "${tocommit:-HEAD}")

mkdir /diff
(cd a && ansible-inventory --list "$@" --output /diff/a.yml)
(cd b && ansible-inventory --list "$@" --output /diff/b.yml)

python /bin/ansible-inventory-diff.py ${verbose:-} /diff/a.yml /diff/b.yml
