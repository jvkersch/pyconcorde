#!/bin/bash
#
# Build Concorde for Linux

set -euxo pipefail

QSOPT_LIB=https://www.math.uwaterloo.ca/~bico/qsopt/beta/codes/PIC/qsopt.PIC.a
QSOPT_INCLUDE=https://www.math.uwaterloo.ca/~bico/qsopt/beta/codes/PIC/qsopt.h
CONCORDE_SRC=https://www.math.uwaterloo.ca/tsp/concorde/downloads/codes/src/co031219.tgz

curl $CONCORDE_SRC -o concorde.tgz
tar xvfz concorde.tgz
cd concorde
curl -o qsopt.a $QSOPT_LIB
curl -O $QSOPT_INCLUDE

CFLAGS="-fPIC -O3 -g" ./configure --with-qsopt=$PWD
make -j4

# Run a small program
TSP/concorde -s 1234 -k 5

# Move the solver to the repo
mkdir -p ../../binaries/linux
mv TSP/concorde ../../binaries/linux/concorde

# Cleanup
cd ..
rm -rf concorde concorde.tgz
