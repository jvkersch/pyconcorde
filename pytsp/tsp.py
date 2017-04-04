# -*- coding: utf-8 -*-
from __future__ import division, print_function

import os
import shutil
import tempfile
import uuid

from pytsp._concorde import _CCdatagroup, _CCutil_gettsplib, _CCtsp_solve_dat
from pytsp.util import write_tsp_file


class ConcordeDataGroup(object):
    """
    TODO expose a way to get the data out again.
    TODO write tests
    """

    def __init__(self):
        self._data = None
        self._ncount = -1

    @classmethod
    def from_tspfile(cls, fname):
        ncount, data = _CCutil_gettsplib(fname)
        if data is None:
            raise RuntimeError("Error in loading {}".format(fname))
        self = cls()
        self._ncount = ncount
        self._data = data
        return self

    @classmethod
    def from_data(cls, xs, ys, norm, name=None):
        """ Construct datagroup from given data.

        This routine writes the given data to a temporary file, and then uses
        Concorde's file parser to read from file and do the initialization.
        """
        # TODO: properly figure out Concorde's CCdatagroup format and
        # initialize this object directly.
        if name is None:
            name = uuid.uuid4().hex
        try:
            ccdir = tempfile.mkdtemp()
            ccfile = os.path.join(ccdir, 'data.tsp')
            with open(ccfile, 'w') as fp:
                write_tsp_file(fp, xs, ys, norm, name)
            return cls.from_tspfile(ccfile)
        finally:
            shutil.rmtree(ccdir)

    @property
    def x(self):
        return self._data.x

    @property
    def y(self):
        return self._data.y

    def __str__(self):
        if self._data is None:
            return "Uninitialized ConcordeDataGroup"
        else:
            return "ConcordeDataGroup with {} nodes".format(self._ncount)


# class ConcordeSolver(object):

#     def __init__(self):
#         pass

#     @classmethod
#     def from_file(cls, fname):
        
