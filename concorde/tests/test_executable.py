import gzip
import os
import unittest
from unittest.mock import patch

from concorde.testing import ConcordeTestMixin, temp_folder
from ..executable import (
    ConcordeNotFoundError,
    check_concorde_executable,
    download_concorde,
)


class TestCheckConcordeExecutable(ConcordeTestMixin, unittest.TestCase):
    def test_check_passes(self):
        # When/then
        try:
            check_concorde_executable("concorde")
        except Exception as e:
            self.fail(f"Unexpected failure: {e}")

    def test_check_fails(self):
        # When/then
        with self.assertRaises(ConcordeNotFoundError):
            check_concorde_executable("hopefully_this_does_not_exist")


class TestDownloadConcorde(unittest.TestCase):
    @temp_folder(chdir=True)
    def test_download(self, _):
        # When
        with patch("concorde.executable.urlretrieve") as mock_retrieve:
            with patch("builtins.print") as mock_print:
                mock_retrieve.side_effect = self._download_concorde
                concorde = download_concorde()

        # Then
        mock_print.assert_called_once()
        mock_retrieve.assert_called_once()
        self.assertTrue(os.path.exists(concorde))

    def _download_concorde(self, location, fname):
        with gzip.open(fname, "wb") as fp:
            fp.write(b"DUMMY DATA")
