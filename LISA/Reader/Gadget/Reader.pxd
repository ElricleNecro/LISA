import numpy as np
cimport numpy as np

from libc.stdio  cimport FILE

cdef struct io_header:
    int        npart[6]
    double        mass[6]
    double        time
    double        redshift
    int        flag_sfr
    int        flag_feedback
    unsigned int    npartTotal[6]
    int        flag_cooling
    int        num_files
    double        BoxSize
    double        Omega0
    double        OmegaLambda
    double        HubbleParam
    int        flag_stellarage
    int        flag_metals
    unsigned int    npartTotalHighWord[6]
    int        flag_entropy_instead_u
    char        fill[60]
ctypedef io_header Header

cdef class GadgetReader:
    cdef Header _header
    cdef _filename
    cdef _nb_files
    cdef _pos
    cdef _vel
    #cpdef Write
    #cpdef Read
    cdef _read_block(self, void *var, int size, int nb, FILE *fd)
    cpdef int _write_format1(self)
    cpdef int _write_format2(self)
    cpdef _read_format1(self, bint bpot=?, bint bacc=?, bint bdadt=?, bint bdt=?)
    #cpdef _read_format2(self, int num_files, bint bpot=?, bint bacc=?, bint bdadt=?, bint bdt=?)

