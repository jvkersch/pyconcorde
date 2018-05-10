""" Concorde base layer.

Cython wrappers around Concorde API.

"""
import numpy as np
cimport numpy as np

cdef extern from "concorde.h":
    struct CCdatagroup:
        double *x
        double *y
        double *z

    struct CCrandstate:
        pass

    int CCutil_gettsplib(char *datname, int *ncount, CCdatagroup *dat)

    int CCtsp_solve_dat (int ncount, CCdatagroup *indat, int *in_tour,
        int *out_tour, double *in_val, double *optval, int *success,
        int *foundtour, char *name, double *timebound, int *hit_timebound,
        int silent, CCrandstate *rstate)

    double CCutil_real_zeit()
    void CCutil_sprand (int seed, CCrandstate *r)

    void CCutil_freedatagroup (CCdatagroup *dat)


cdef class _CCdatagroup:

    cdef CCdatagroup c_data
    cdef bint initialized
    cdef int ncount

    def __cinit__(self):
        self.initialized = False

    def __dealloc__(self):
        if self.initialized:
            CCutil_freedatagroup(&(self.c_data))

    @property
    def x(self):
        cdef double[:] x_data
        if self.initialized:
            x_data = <double[:self.ncount]>self.c_data.x
            return np.asarray(x_data)
        else:
            return np.array([])

    @property
    def y(self):
        cdef double[:] y_data
        if self.initialized:
            y_data = <double[:self.ncount]>self.c_data.y
            return np.asarray(y_data)
        else:
            return np.array([])

    @property
    def z(self):
        cdef double[:] y_data
        if self.initialized:
            z_data = <double[:self.ncount]>self.c_data.z
            return np.asarray(z_data)
        else:
            return np.array([])


def _CCutil_gettsplib(str fname):
    cdef int ncount, retval
    cdef _CCdatagroup dat

    dat = _CCdatagroup()

    retval = CCutil_gettsplib(fname.encode('utf-8'), &ncount, &dat.c_data)
    if retval == 0:
        dat.initialized = True
        dat.ncount = ncount
        return ncount, dat
    else:
        return -1, None


def _CCtsp_solve_dat(
        int ncount, _CCdatagroup ingroup,
        str name, double timebound, int silent, int seed=0):

    cdef:
        int *in_tour = NULL
        double *in_val = NULL      # initial upper bound
        double opt_val = 0         # value of the optimal tour
        int success = 0            # set to 1 if the run finishes normally
        int foundtour = 0          # set to 1 if a tour has been found
        double *_timebound = NULL  # NULL if no timebound, >= 0 otherwise
        int hit_timebound = 0
        int retval

        # Random state used by the solver
        CCrandstate rstate

        # Output tour
        np.ndarray[int, ndim=1] out_tour

    out_tour = np.zeros(ncount, dtype=np.int32)

    if seed != 0:
        seed = <int>CCutil_real_zeit()
    CCutil_sprand (seed, &rstate)

    if timebound > 0:
        _timebound = &timebound

    retval = CCtsp_solve_dat(ncount, &ingroup.c_data, in_tour, &out_tour[0],
                             in_val, &opt_val, &success, &foundtour,
                             name.encode('utf-8'), _timebound, &hit_timebound,
                             silent, &rstate)

    return out_tour, opt_val, bool(success), bool(foundtour), bool(hit_timebound)
