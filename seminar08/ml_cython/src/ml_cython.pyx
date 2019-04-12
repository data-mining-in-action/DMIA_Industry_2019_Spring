#!python
#cython: language_level=3

import numpy as np

cimport numpy as np
cimport cython

cdef extern from "stdlib.h":
     int c_libc_rand "rand"()

@cython.boundscheck(False)
@cython.wraparound(False)
def func1():
    np.random.seed(42)
    cdef np.ndarray[np.float64_t] result = np.zeros(10000, dtype=np.float64)
    cdef int i
    for i in range(10000):
        result[i] = (np.random.randint(0, 2, size=10000) * 2 - 1).mean()
    return result


@cython.boundscheck(False)
@cython.wraparound(False)
def func2():   
    np.random.seed(42)
    cdef np.ndarray[np.float64_t] result = np.zeros(10000, dtype=np.float64)
    cdef np.float64_t val
    cdef int i, j
    for i in range(10000):
        val = 0
        for j in range(10000):
            val += c_libc_rand() % 2 * 2 - 1
        result[i] = val / 10000.
    return result
