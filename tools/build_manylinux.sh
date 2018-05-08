#!/bin/bash
#
# Build script for manylinux1. Run this with
# sudo docker run -ti -v `pwd`:/io --rm \
#    quay.io/pypa/manylinux1_x86_64 \
#    /bin/bash -c "cd /io && ./tools/build_manylinux.sh"

set -e

git clean -fdx .
tools/build_concorde.sh

TAGS="cp27-cp27m cp27-cp27mu cp35-cp35m cp36-cp36m"
for tag in $TAGS; do
    echo "Building for $tag"
    PREFIX=/opt/python/$tag/bin
    $PREFIX/pip install numpy cython
    $PREFIX/python setup.py bdist_wheel
done
