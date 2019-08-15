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
  echo "Usage: $0 [-v] <commitish> [--to <commitish>] [group]"
  exit
fi

mkdir /src && cd /src
# Fix refs to match /git
git clone -nqs /git a && rm -rf a/.git/refs && cp -r /git/.git/refs /git/.git/config a/.git
(cd a && git reset -q --hard "${commit}")

if [ -n "${tocommit:-}" ]; then
  git clone -nqs /git b && rm -rf b/.git/refs && cp -r /git/.git/refs /git/.git/config b/.git
  (cd b && git reset -q --hard "${tocommit}")
else
  # allow comparison of uncommitted changes
  ln -s /git b
fi


mkdir /diff
(cd a && ansible-inventory --list "$@" --output /diff/a.yml)
(cd b && ansible-inventory --list "$@" --output /diff/b.yml)

ansible-inventory-diff ${verbose:-} /diff/a.yml /src/a /diff/b.yml /src/b
