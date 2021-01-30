import subprocess
import unittest

from ..concorde_test_mixin import ConcordeTestMixin


class TestConcordeTestMixin(ConcordeTestMixin, unittest.TestCase):
    def test_setup(self):
        # When/then
        self._check_can_invoke("concorde", ["-h"])

    def _check_can_invoke(self, cmd, args):
        try:
            subprocess.run(
                [cmd] + args,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception as e:
            self.fail(f"Could not run command. Error: {e}")
