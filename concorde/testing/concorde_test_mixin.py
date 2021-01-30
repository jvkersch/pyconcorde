import os
import shutil
import stat
import textwrap
import tempfile


def _write_dummy_concorde_runner(path: str):
    """ Write a script that can invoke the dummy concorde runner.

    The tests cannot just invoke dummy_concorde.py, since the
    that module may be part of a zip file.

    """
    with open(path, "wt") as fp:
        fp.write(
            textwrap.dedent(
                """\
            #!/bin/bash
            set -euxo pipefail
            python -m concorde.testing.dummy_concorde "$@"
        """
            )
        )
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)


class ConcordeTestMixin:
    """ Mixin class that makes the dummy concorde available on the path.
    """

    def setUp(self):
        # Create temp folder
        self._concorde_folder = folder = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, folder)

        # Install script runner
        concorde_path = os.path.join(folder, "concorde")
        _write_dummy_concorde_runner(concorde_path)

        # Add to path
        oldpath = os.environ["PATH"]
        os.environ["PATH"] = folder + os.pathsep + oldpath

        def _reset_path():
            os.environ["PATH"] = oldpath

        self.addCleanup(_reset_path)
