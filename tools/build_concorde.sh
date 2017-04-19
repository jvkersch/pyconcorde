#!/bin/bash

# Helper script to build concorde on a Linux platform. This is mainly useful
# for Travis CI, although it can be used elsewhere, too.

set -e

# Static libraries and headers. This will be uploaded to Travis' cache.
DATA="$HOME/data"
mkdir -p "$DATA/"{lib,include}
# Temporary build directory. This won't get cached.
BUILD="$HOME/build"
mkdir -p "$BUILD"

function download_qsopt() {
    if [ ! -f "$DATA/lib/qsopt.a" ]; then
	curl -o "$DATA/lib/qsopt.a" \
	     http://www.math.uwaterloo.ca/~bico/qsopt/beta/codes/PIC/qsopt.PIC.a
	ln -fs "$DATA/lib/qsopt.a" "$DATA/qsopt.a"
    fi
    if [ ! -f "$DATA/include/qsopt.h" ]; then
	curl -o "$DATA/include/qsopt.h" \
	     http://www.math.uwaterloo.ca/~bico/qsopt/beta/codes/PIC/qsopt.h
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
    if [ ! -f "$DATA/concorde.a" ]; then
	DATAFOLDER=$(readlink -f "$DATA")
	(cd "$BUILD/concorde" && \
	     CFLAGS="-fPIC -O2 -g" ./configure --prefix "$DATAFOLDER" --with-qsopt="$DATAFOLDER" && \
	     make)
        mv "$BUILD/concorde/concorde.a" "$DATA/lib"
        mv "$BUILD/concorde/concorde.h" "$DATA/include"
    fi
}


download_qsopt
download_concorde
build_concorde
