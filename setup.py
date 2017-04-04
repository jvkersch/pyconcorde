import os
from os.path import dirname
import glob

import setuptools  # noqa

from Cython.Build import cythonize
from distutils.core import setup
from distutils.extension import Extension

import numpy as np


def get_concorde_base_dir():
    # Environment variable
    concorde_dir = os.environ.get('CONCORDE_DIR')
    if concorde_dir is not None:
        return concorde_dir
    # Homebrew
    for location in glob.glob("/usr/local/Cellar/concorde/*/lib/concorde.a"):
        concorde_dir = dirname(dirname(location))
        return concorde_dir
    # That's it, we're all out of ideas
    raise RuntimeError(
        "Install Concorde and set the CONCORDE_DIR environment variable "
        "to point to the Concorde base folder."
    )


def get_qsopt_base_dir():
    # Environment variable
    qsopt_dir = os.environ.get('QSOPT_DIR')
    if qsopt_dir is not None:
        return qsopt_dir
    # Homebrew
    for location in glob.glob("/usr/local/Cellar/qsopt/*/lib/qsopt.a"):
        qsopt_dir = dirname(dirname(location))
        return qsopt_dir
    # That's it, we're all out of ideas
    raise RuntimeError(
        "Install Qsopt and set the QSOPT_DIR environment variable "
        "to point to the Qsopt base folder."
    )


CONCORDE_DIR = get_concorde_base_dir()
QSOPT_DIR = get_qsopt_base_dir()


setup(
    name='pytsp',
    ext_modules=cythonize([
        Extension(
            'pytsp._concorde',
            sources=["pytsp/_concorde.pyx"],
            include_dirs=[os.path.join(CONCORDE_DIR, "include"),
                          np.get_include()],
            extra_objects=[
                os.path.join(CONCORDE_DIR, "lib", "concorde.a"),
                os.path.join(QSOPT_DIR, "lib", "qsopt.a"),
            ])
        ]),
    version='0.1.0',
    install_requires=[
        'cython>=0.22.0',
    ]
)
