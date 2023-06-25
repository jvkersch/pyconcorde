#!/bin/bash
#
# Build Concorde for arm64

set -euxo pipefail

QSOPT_LIB=https://www.math.uwaterloo.ca/~bico/qsopt/downloads/codes/m1/qsopt.a
QSOPT_INCLUDE=https://www.math.uwaterloo.ca/~bico/qsopt/downloads/codes/m1/qsopt.h
CONCORDE_SRC=https://www.math.uwaterloo.ca/tsp/concorde/downloads/codes/src/co031219.tgz

curl $CONCORDE_SRC -o concorde.tgz
tar xvfz concorde.tgz
cd concorde
curl -O $QSOPT_LIB
curl -O $QSOPT_INCLUDE

CFLAGS="-target arm64-apple-darwin20.1.0 -fPIC -O2 -g" ./configure --with-qsopt=$PWD --host=darwin
make -j4

# Run a small program. Ignore status code if this fails (script is meant to run
# inside a GitHub actions worker, which is Intel)
TSP/concorde -s 1234 -k 5 || true

# Move the solver to the repo
mkdir -p ../../binaries/macos/arm64
mv TSP/concorde ../../binaries/macos/arm64/concorde

# Cleanup
cd ..
rm -rf concorde concorde.tgz
