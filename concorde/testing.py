from functools import wraps
import tempfile


def temp_folder():
    def inner(fn):
        @wraps(fn)
        def wrapper(self, *args, **kwds):
            with tempfile.TemporaryDirectory() as folder:
                return fn(self, folder, *args, **kwds)

        return wrapper

    return inner
