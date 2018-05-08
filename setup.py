from __future__ import print_function, unicode_literals

from functools import partial
import glob
import os
from os.path import dirname, exists, join as pjoin
import shutil
import subprocess
import sys

try:
    import urllib.request
    urlretrieve = urllib.request.urlretrieve
except ImportError:  # python 2
    import urllib.urlretrieve as urlretrieve

import setuptools  # noqa

from Cython.Build import cythonize
from distutils.core import setup
from distutils.extension import Extension

import numpy as np

QSOPT_LOCATION = {
    "darwin": (
        "https://www.math.uwaterloo.ca/~bico/qsopt/beta/codes/mac64/qsopt.a",
        "https://www.math.uwaterloo.ca/~bico/qsopt/beta/codes/mac64/qsopt.h"
    ),
    "linux": (
        "http://www.math.uwaterloo.ca/~bico/qsopt/beta/codes/PIC/qsopt.PIC.a",
        "http://www.math.uwaterloo.ca/~bico/qsopt/beta/codes/PIC/qsopt.h"
    )
}

CONCORDE_SRC = "http://www.math.uwaterloo.ca/tsp/concorde/downloads/codes/src/co031219.tgz"  # noqa


def validate_folder(path, required_fnames):
    missing = set()
    for fname in required_fnames:
        f =  os.path.isfile(os.path.join(path, fname))
        print(os.path.join(path, fname))
        if not f:
            missing.add(fname)
    if missing:
        raise RuntimeError("In folder {}: missing {}".format(
            path, ', '.join(missing)))
    return path


def get_concorde_base_dir():
    v = partial(validate_folder,
                required_fnames=['include/concorde.h', 'lib/concorde.a'])
    # Environment variable
    concorde_dir = os.environ.get('CONCORDE_DIR')
    if concorde_dir is not None:
        return v(concorde_dir)
    # Homebrew
    for location in glob.glob("/usr/local/Cellar/concorde/*/lib/concorde.a"):
        concorde_dir = dirname(dirname(location))
        return v(concorde_dir)
    # ./data
    concorde_dir = os.path.normpath("data")
    if os.path.exists(concorde_dir):
        return v(concorde_dir)
    # That's it, we're all out of ideas
    raise RuntimeError(
        "Install Concorde and set the CONCORDE_DIR environment variable "
        "to point to the Concorde base folder."
    )


def get_qsopt_base_dir():
    v = partial(validate_folder,
                required_fnames=['include/qsopt.h', 'lib/qsopt.a'])
    # Environment variable
    qsopt_dir = os.environ.get('QSOPT_DIR')
    if qsopt_dir is not None:
        return v(qsopt_dir)
    # Homebrew
    for location in glob.glob("/usr/local/Cellar/qsopt/*/lib/qsopt.a"):
        qsopt_dir = dirname(dirname(location))
        return v(qsopt_dir)
    # ./data
    qsopt_dir = os.path.normpath("data")
    if os.path.exists(qsopt_dir):
        return v(qsopt_dir)
    # That's it, we're all out of ideas
    raise RuntimeError(
        "Install Qsopt and set the QSOPT_DIR environment variable "
        "to point to the Qsopt base folder."
    )


# CONCORDE_DIR = get_concorde_base_dir()
# QSOPT_DIR = get_qsopt_base_dir()
# print('CONCORDE_DIR = {}'.format(CONCORDE_DIR))
# print('QSOPT_DIR = {}'.format(QSOPT_DIR))


def _safe_makedirs(*paths):
    for path in paths:
        try:
            os.makedirs(path)
        except os.error:
            pass


def download_concorde_qsopt():
    _safe_makedirs("data")
    _safe_makedirs("build")
    qsopt_a_path = pjoin("data", "qsopt.a")
    qsopt_h_path = pjoin("data", "qsopt.h")
    if not exists(qsopt_a_path) or not exists(qsopt_h_path):
        print("qsopt is missing, downloading")
        qsopt_a_url, qsopt_h_url = QSOPT_LOCATION[sys.platform]
        urlretrieve(qsopt_a_url, qsopt_a_path)
        urlretrieve(qsopt_h_url, qsopt_h_path)
    concorde_src_path = pjoin("build", "concorde.tgz")
    if not exists(concorde_src_path):
        print("concorde is missing, downloading")
        urlretrieve(CONCORDE_SRC, concorde_src_path)


def _run(cmd, cwd):
    subprocess.check_call(cmd, shell=True, cwd=cwd)


def build_concorde():
    if (not exists("data/include/concorde.h") or
        not exists("data/lib/concorde.a")):
        print("building concorde")
        _run("tar xzvf concorde.tgz", "build")

        cflags = "-fPIC -O2 -g"

        if sys.platform.startswith("darwin"):
            flags += "--host=darwin"
        else:
            flags = ""

        datadir = os.path.abspath("data")
        cwd = ('CFLAGS="{cflags}" ./configure --prefix {data} '
               '--with-qsopt={data} {flags}').format(
                   cflags=cflags,
                   data=datadir,
                   flags=flags
               )

        _run(cwd, "build/concorde")
        _run("make", "build/concorde")

        _safe_makedirs("data/lib", "data/include")
        shutil.copyfile("build/concorde/concorde.a",
                        "data/lib/concorde.a")
        shutil.copyfile("build/concorde/concorde.h",
                        "data/include/concorde.h")


setup(
    name='pyconcorde',
    ext_modules=cythonize([
        Extension(
            'concorde._concorde',
            sources=["concorde/_concorde.pyx"],
            include_dirs=[os.path.join(CONCORDE_DIR, "include"),
                          np.get_include()],
            extra_objects=[
                os.path.join(CONCORDE_DIR, "lib", "concorde.a"),
                os.path.join(QSOPT_DIR, "lib", "qsopt.a"),
            ],
        )
    ]),
    version='0.1.0',
    install_requires=[
        'cython>=0.22.0',
        'numpy>=1.10.0',
    ],
    license='BSD',
    author='Joris Vankerschaver',
    author_email='joris.vankerschaver@gmail.com',
    url='https://github.com/jvkersch/pyconcorde',
    description='Cython wrappers for the Concorde TSP library',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: BSD License",
    ],
)
