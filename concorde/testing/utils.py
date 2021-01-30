import os
import contextlib
from io import StringIO
from functools import wraps
import sys
import tempfile


def temp_folder(chdir=False):
    def inner(fn):
        @wraps(fn)
        def wrapper(self, *args, **kwds):
            with tempfile.TemporaryDirectory() as folder:
                cm = cd(folder) if chdir else contextlib.nullcontext
                with cm:
                    return fn(self, folder, *args, **kwds)

        return wrapper

    return inner


@contextlib.contextmanager
def cd(folder):
    old_cwd = os.getcwd()
    try:
        os.chdir(folder)
        yield
    finally:
        os.chdir(old_cwd)
