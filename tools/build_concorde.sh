#!/bin/bash

# Helper script to build concorde on a Linux platform. This is mainly useful
# for Travis CI, although it can be used elsewhere, too.

set -e

# Static libraries and headers. This will be uploaded to Travis' cache.
DATA="$PWD/data"
mkdir -p "$DATA/"{lib,include}
# Temporary build directory. This won't get cached.
BUILD="$PWD/build"
mkdir -p "$BUILD"

# Configure flags
PLATFORM=$(uname)
if [[ "$PLATFORM" == "Darwin" ]]; then
    FLAGS="--host=darwin"
    QSOPT="https://www.math.uwaterloo.ca/~bico/qsopt/beta/codes/mac64/qsopt.a"
    QSOPT_H="https://www.math.uwaterloo.ca/~bico/qsopt/beta/codes/mac64/qsopt.h"
else
    FLAGS=""
    QSOPT="http://www.math.uwaterloo.ca/~bico/qsopt/beta/codes/PIC/qsopt.PIC.a"
    QSOPT_H="http://www.math.uwaterloo.ca/~bico/qsopt/beta/codes/PIC/qsopt.h"
fi

function download_qsopt() {
    if [ ! -f "$DATA/lib/qsopt.a" ]; then
	curl -o "$DATA/lib/qsopt.a" "$QSOPT"
	ln -fs "$DATA/lib/qsopt.a" "$DATA/qsopt.a"
    fi
    if [ ! -f "$DATA/include/qsopt.h" ]; then
	curl -o "$DATA/include/qsopt.h" "$QSOPT_H"
	ln -fs "$DATA/include/qsopt.h" "$DATA/qsopt.h"
    fi
}

function download_concorde() {
    if [ ! -f "$DATA/lib/concorde.a" ]; then
	curl -o "$BUILD/concorde.tgz" \
	     http://www.math.uwaterloo.ca/tsp/concorde/downloads/codes/src/co031219.tgz
	(cd "$BUILD" && tar xvfz concorde.tgz)
    fi
}

function build_concorde() {
    if [ ! -f "$DATA/lib/concorde.a" ]; then
	(cd "$BUILD/concorde" && \
	     CFLAGS="-fPIC -O2 -g" ./configure \
                   --prefix "$DATA" \
                   --with-qsopt="$DATA" \
                   "$FLAGS" && \
	     make)
        mv "$BUILD/concorde/concorde.a" "$DATA/lib"
        mv "$BUILD/concorde/concorde.h" "$DATA/include"
    fi
}


download_qsopt
download_concorde
build_concorde
