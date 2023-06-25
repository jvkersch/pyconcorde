#!/bin/bash
#
# Build Concorde for arm64

set -euxo pipefail

# Note: despite the name, the static library is actually gzip compressed!
QSOPT_LIB=https://www.math.uwaterloo.ca/~bico/qsopt/downloads/codes/mac64/qsopt.a
QSOPT_INCLUDE=https://www.math.uwaterloo.ca/~bico/qsopt/downloads/codes/mac64/qsopt.h
CONCORDE_SRC=https://www.math.uwaterloo.ca/tsp/concorde/downloads/codes/src/co031219.tgz

curl $CONCORDE_SRC -o concorde.tgz
tar xvfz concorde.tgz
cd concorde
curl -o qsopt.a.gz $QSOPT_LIB
gunzip -f qsopt.a.gz
curl -O $QSOPT_INCLUDE

CFLAGS="-target x86_64-apple-darwin-macho -fPIC -O2 -g" ./configure --with-qsopt=$PWD --host=darwin
make -j4

# Run a small program
TSP/concorde -s 1234 -k 5

# Move the solver to the repo
mkdir -p ../../binaries/macos/x86_64
mv TSP/concorde ../../binaries/macos/x86_64/concorde

# Cleanup
cd ..
rm -rf concorde concorde.tgz
