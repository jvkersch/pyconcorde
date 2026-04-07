"""Custom build command to download and compile Concorde/QSOpt.

By default, the setup script will download the QSOpt linear solver, and
download and compile Concorde. If you have either one of these packages
already installed, you can use the installed version by setting the
following environment variables:

QSOPT_DIR: should point to a folder containing qsopt.a and qsopt.h
CONCORDE_DIR: contains concorde.a and concorde.h

Note that for the build process to work correctly, you should either
not set these variables (and rely on the downloaded Concorde) or set
both of them. Setting only one will not work as intended.

"""

import os
from os.path import exists, join as pjoin
import platform
import shutil
import subprocess
import urllib.request

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext

from Cython.Build import cythonize

import numpy as np

QSOPT_LOCATION = {
    "Darwin": {
        "arm64": (
            "https://www.math.uwaterloo.ca/~bico/qsopt/downloads/codes/m1/qsopt.a",
            "https://www.math.uwaterloo.ca/~bico/qsopt/downloads/codes/m1/qsopt.h",
        ),
        "x86_64": (
            "https://www.math.uwaterloo.ca/~bico/qsopt/downloads/codes/mac64/qsopt.a",
            "https://www.math.uwaterloo.ca/~bico/qsopt/downloads/codes/mac64/qsopt.h",
        ),
    },
    "Linux": {
        "x86_64": (
            "https://www.math.uwaterloo.ca/~bico/qsopt/beta/codes/PIC/qsopt.PIC.a",
            "https://www.math.uwaterloo.ca/~bico/qsopt/beta/codes/PIC/qsopt.h",
        ),
    },
}

CONCORDE_SRC = "https://www.math.uwaterloo.ca/tsp/concorde/downloads/codes/src/co031219.tgz"  # noqa


def _safe_makedirs(*paths):
    for path in paths:
        os.makedirs(path, exist_ok=True)


def download_concorde_qsopt():
    _safe_makedirs("data")
    _safe_makedirs("build")
    qsopt_a_path = pjoin("data", "qsopt.a")
    qsopt_h_path = pjoin("data", "qsopt.h")
    if not exists(qsopt_a_path) or not exists(qsopt_h_path):
        print("qsopt is missing, downloading")
        machine = platform.machine()
        qsopt_a_url, qsopt_h_url = QSOPT_LOCATION[platform.system()][machine]
        urllib.request.urlretrieve(qsopt_a_url, qsopt_a_path)
        urllib.request.urlretrieve(qsopt_h_url, qsopt_h_path)
    concorde_src_path = pjoin("build", "concorde.tgz")
    if not exists(concorde_src_path):
        print("concorde is missing, downloading")
        urllib.request.urlretrieve(CONCORDE_SRC, concorde_src_path)


def _run(cmd, cwd):
    subprocess.check_call(cmd, shell=True, cwd=cwd)


def build_concorde():
    if not exists("data/concorde.h") or not exists("data/concorde.a"):
        print("building concorde")
        _run("tar xzvf concorde.tgz", "build")

        cflags = "-fPIC -O2 -g -std=gnu89"

        if platform.system().startswith("Darwin"):
            flags = "--host=darwin"
        else:
            flags = ""

        datadir = os.path.abspath("data")
        cwd = f'CFLAGS="{cflags}" ./configure --prefix {datadir} --with-qsopt={datadir} {flags}'

        _run(cwd, "build/concorde")
        _run("make", "build/concorde")

        shutil.copyfile("build/concorde/concorde.a", "data/concorde.a")
        shutil.copyfile("build/concorde/concorde.h", "data/concorde.h")


class build_ext(_build_ext):
    """Build command that downloads and installs Concorde, if not found."""

    def run(self):
        if not self.has_external_concorde:
            download_concorde_qsopt()
            build_concorde()
        else:
            print("Using external Concorde/QSOpt")

        super().run()

    @property
    def has_external_concorde(self):
        qsopt_dir = os.environ.get("QSOPT_DIR")
        concorde_dir = os.environ.get("CONCORDE_DIR")
        return bool(qsopt_dir) and bool(concorde_dir)


class ConcordeExtension(Extension):
    """Extension that sets Concorde/QSOpt lib/include args."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        qsopt_dir = os.environ.get("QSOPT_DIR", "data")
        concorde_dir = os.environ.get("CONCORDE_DIR", "data")
        self.include_dirs.append(concorde_dir)
        self.extra_objects.extend(
            [pjoin(qsopt_dir, "qsopt.a"), pjoin(concorde_dir, "concorde.a")]
        )


setup(
    ext_modules=cythonize(
        [
            ConcordeExtension(
                "concorde._concorde",
                sources=["concorde/_concorde.pyx"],
                include_dirs=[np.get_include()],
            )
        ]
    ),
    cmdclass={
        "build_ext": build_ext,
    },
)
