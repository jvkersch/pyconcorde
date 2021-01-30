import stat
import platform
import shutil
import gzip
import os
import subprocess
import tempfile
from urllib.request import urlretrieve


_NOT_FOUND_MESSAGE = (
    "Could not run the concorde executable at {!r}. Check that the concorde "
    "executable is present and can be run."
)

_CONCORDE_EXE = {
    "linux": "http://www.math.uwaterloo.ca/tsp/concorde/downloads/codes/linux24/concorde.gz"  # noqa
}


class ConcordeNotFoundError(Exception):
    def __init__(self, concorde):
        super().__init__(_NOT_FOUND_MESSAGE.format(concorde))


def check_concorde_executable(concorde: str):
    """ Check that the concorde executable can be run.
    """
    cmd = [
        os.path.expanduser(concorde),
        "-s",
        "1234",
        "-k",
        "5",
    ]  # random problem with 5 nodes
    try:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                cmd,
                check=True,
                cwd=tmp,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
    except (FileNotFoundError, subprocess.CalledProcessError):
        raise ConcordeNotFoundError(concorde) from None


def download_concorde() -> str:
    """ Download concorde executable for the current platform.
    """
    p = platform.system().lower()
    location = _CONCORDE_EXE[p]
    basename_gz = os.path.basename(location)
    basename, _ = os.path.splitext(basename_gz)

    urlretrieve(location, basename_gz)

    try:
        with gzip.open(basename_gz, "rb") as gzipped:
            with open(basename, "wb") as concorde:
                shutil.copyfileobj(gzipped, concorde)
    finally:
        os.unlink(basename_gz)

    # Set the executable bit
    st = os.stat(basename)
    os.chmod(basename, st.st_mode | stat.S_IEXEC)

    print(
        f"Concorde downloaded to the current directory (file {basename!r}). "
        f"Please add this executable to a location on the path."
    )

    return basename
