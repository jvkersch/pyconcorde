import os
from os.path import dirname
from functools import partial
import glob

import setuptools  # noqa

from Cython.Build import cythonize
from distutils.core import setup
from distutils.extension import Extension

import numpy as np


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
    v = partial(validate_folder, required_fnames=['include/concorde.h', 'lib/concorde.a'])
    # Environment variable
    concorde_dir = os.environ.get('CONCORDE_DIR')
    if concorde_dir is not None:
        return v(concorde_dir)
    # Homebrew
    for location in glob.glob("/usr/local/Cellar/concorde/*/lib/concorde.a"):
        concorde_dir = dirname(dirname(location))
        return v(concorde_dir)
    # $HOME/data
    concorde_dir = os.path.normpath(os.path.expanduser("~/data"))
    if os.path.exists(concorde_dir):
        return v(concorde_dir)
    # That's it, we're all out of ideas
    raise RuntimeError(
        "Install Concorde and set the CONCORDE_DIR environment variable "
        "to point to the Concorde base folder."
    )


def get_qsopt_base_dir():
    v = partial(validate_folder, required_fnames=['qsopt.h', 'qsopt.a'])
    # Environment variable
    qsopt_dir = os.environ.get('QSOPT_DIR')
    if qsopt_dir is not None:
        return v(qsopt_dir)
    # Homebrew
    for location in glob.glob("/usr/local/Cellar/qsopt/*/lib/qsopt.a"):
        qsopt_dir = dirname(dirname(location))
        return v(qsopt_dir)
    # $HOME/data
    qsopt_dir = os.path.normpath(os.path.expanduser("~/data"))
    if os.path.exists(qsopt_dir):
        return v(qsopt_dir)
    # That's it, we're all out of ideas
    raise RuntimeError(
        "Install Qsopt and set the QSOPT_DIR environment variable "
        "to point to the Qsopt base folder."
    )


CONCORDE_DIR = get_concorde_base_dir()
QSOPT_DIR = get_qsopt_base_dir()
print('CONCORDE_DIR = {}'.format(CONCORDE_DIR))
print('QSOPT_DIR = {}'.format(QSOPT_DIR))


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
            ],
        )
    ]),
    version='0.1.0',
    install_requires=[
        'cython>=0.22.0',
    ]
)
