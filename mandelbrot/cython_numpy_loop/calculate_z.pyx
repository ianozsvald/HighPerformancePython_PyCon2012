"""
Mandelbrot Cython
-----------------
This code uses complex numbers requiring a recent version of Cythnon > 0.11.2
Attribution: Didrik Pinte (Enthought) for first version for first version
Converted to look like the others in this set by Ian Ozsvald
"""

from cython.parallel import prange

from numpy import empty
cimport numpy as np
cimport cython

# change required for prange (OpenMP) support:
# Set boundscheck(False) else Cython complains on z[i], requires cimport cython
# note that boundscheck(False) doesn't change speed of normal Python version
# added cdef unsigned int lengthq = len(q)
# added prange(lengthq, nogil=True)

#@cython.boundscheck(False) # only required for prange support
def calculate_z(np.ndarray[double complex, ndim=1] q, int maxiter, np.ndarray[double complex, ndim=1] z):
    """ Generate a mandelbrot set """
    cdef unsigned int i
    cdef unsigned int iteration
    cdef double zx, zy, qx, qy, zx_new, zy_new

    cdef np.ndarray[int, ndim=1] output = empty(dtype='i', shape=(len(q)))
    cdef unsigned int lengthq = len(q)

    # openMP variant (multithreaded at the OS level)
    #for i in prange(lengthq, nogil=True):
    #for i in prange(lengthq, nogil=True, schedule='dynamic'):
    # normal Python version (single threaded)
    for i in range(lengthq):
        zx = z[i].real # need to extract items using dot notation
        zy = z[i].imag
        qx = q[i].real
        qy = q[i].imag

        for iteration in range(maxiter):
            zx_new = (zx * zx - zy * zy) + qx
            zy_new = (zx * zy + zy * zx) + qy
            # must assign after else we're using the new zx/zy in the fla
            zx = zx_new
            zy = zy_new
            if (zx*zx + zy*zy) > 4.0:
                output[i] = iteration
                break
    return output
