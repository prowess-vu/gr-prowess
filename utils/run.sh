#!/bin/sh

if [ $# -lt 1 ]; then
  echo "Usage: ./run.sh [PATH_TO_FLOWGRAPH.py] [OPTIONS]"
  exit 1
elif [ ! -f "$1" ]; then
  echo "Invalid file: $1"
  exit 2
fi

sudo cset shield --userset=prowess --exec -- python3 "$@"
