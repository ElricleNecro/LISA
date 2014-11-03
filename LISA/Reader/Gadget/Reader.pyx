cimport cython
cimport Reader as g

import numpy as np
cimport numpy as np

from libc.stdlib cimport malloc, calloc, free
from libc.stdio  cimport fread, fwrite, FILE, fopen, fclose, stderr, fprintf

#class ReadError():
    #pass

cdef class GadgetReader:
    def __cinit__(self, *args, **kwargs):
        pass

    @cython.boundscheck(False)
    def __init__(self, filename, numfile=1):
        cdef unsigned int i
        self._filename  = filename
        self._nb_files = numfile

        for i in range(6):
            self._header.npart[i]              = 0
            self._header.mass[i]               = 0.
            self._header.npartTotalHighWord[i] = 0

        self._header.time                   = 0.
        self._header.num_files              = numfile
        self._header.redshift               = 0.
        self._header.flag_sfr               = 0
        self._header.flag_feedback          = 0
        self._header.flag_cooling           = 0
        self._header.BoxSize                = 0.
        self._header.Omega0                 = 0.
        self._header.OmegaLambda            = 0.
        self._header.HubbleParam            = 0.
        self._header.flag_stellarage        = 0
        self._header.flag_metals            = 0
        self._header.flag_entropy_instead_u = 0

    def __repr__(self):
        return  """Gadget file '{0}'. Header informations are:
Simulation parameters:
    Time       : {1}
    num_files  : {2}
    redshift   : {3}
    BoxSize    : {4}
    Particules : {5}
    Masses     : {6}
Physical parameters:
    Omega0      : {7}
    OmegaLambda : {8}
    HubbleParam : {9}
Simulation flags:
    flag_sfr               : {10}
    flag_feedback          : {11}
    flag_cooling           : {12}
    flag_stellarage        : {13}
    flag_metals            : {14}
    flag_entropy_instead_u : {15}
The only gadget file format supported is the gadget 1.
            """.format(
                self.filename,
                self.header.time,
                self.header.num_files,
                self.header.redshift,
                self.header.BoxSize,
                self.npart,
                self.mass,
                self.header.Omega0,
                self.header.OmegaLambda,
                self.header.HubbleParam,
                self.header.flag_sfr,
                self.header.flag_feedback,
                self.header.flag_cooling,
                self.header.flag_stellarage,
                self.header.flag_metals,
                self.header.flag_entropy_instead_u,
            )

    def __str__(self):
        return self.__repr__()

    #def __dealloc__(self):
        #free(self.part_pos)
        #free(self.part_vel)

    cpdef int _write_format1(self):
        cdef int res
        cdef unsigned int i
        cdef char *fname = self.filename
        #if self.part.ptr_data == NULL:
            #raise MemoryError("Particules array not allocate.")
        for i in range(6):
            self.header.npartTotal[i] = self.header.npart[i]
        #res = g.Double_Gadget_Write_format1(fname, self.header, self.part.ptr_data)
        return res

    cpdef int _write_format2(self):
        cdef int res
        cdef unsigned int i
        cdef char *fname = self.filename
        #if self.part.ptr_data == NULL:
            #raise MemoryError("Particules array not allocate.")
        for i in range(6):
            self.header.npartTotal[i] = self.header.npart[i]
        #res = g.Double_Gadget_Write_format2(fname, self.header, self.part.ptr_data)
        return res

    cdef _read_block(self, void *var, int size, int nb, FILE *fd):
        cdef:
            int dummy, dummy2

        fread(&dummy, sizeof(dummy), 1, fd)
        fread(var, size, nb, fd)
        fread(&dummy2, sizeof(dummy), 1, fd)

        if dummy != dummy2:
            raise MemoryError #ReadError("Bad reading while reading header.")

    cpdef _read_format1(self, bint bpot=0, bint bacc=0, bint bdadt=0, bint bdt=0):
        cdef:
            FILE *fd = NULL
            int N = 0
            int dummy, dummy2
            int i, j, k, ntot_withmasses = 0
            int n, pc, pc_new, pc_sph
            int NumPart = 0
            char *fname
            np.ndarray[float, ndim=1, mode="c"] _pos, _vel

        for i in range(self._nb_files):
            if self.num_files != 1:
                filename = self._filename + ".%d"%i
                fname    = filename
            else:
                fname    = self._filename

            fd = fopen(fname, "r")
            if fd is NULL:
                raise FileNotFoundError(filename)
            fprintf(stderr, "File open")

            self._read_block(&self._header, sizeof(self._header), 1, fd)
            fprintf(stderr, "Bloc lu.")

            if self._nb_files == 1:
                for j in range(6):
                    NumPart += self._header.npart[j]
            else:
                for j in range(6):
                    NumPart += self._header.npartTotal[j]

            for j in range(6):
                if self._header.mass[j] == 0:
                    ntot_withmasses += self._header.npart[j]

            if i == 0:
                fprintf(stderr, "Begin init")
                _pos = np.empty(3*NumPart, dtype=np.float32)
                fprintf(stderr, "Toto")
                _vel = np.empty(3*NumPart, dtype=np.float32)
                fprintf(stderr, "End init")

            self._read_block(<float*>_pos.data, sizeof(float), 3*NumPart, fd)
            self._read_block(<float*>_vel.data, sizeof(float), 3*NumPart, fd)

            fclose(fd)

        self._pos = _pos
        self._vel = _vel

    #cpdef _read_format2(self, bint bpot=0, bint bacc=0, bint bdadt=0, bint bdt=0):
        #cdef int N = 0
        #cdef unsigned int i
        #cdef char *fname = <bytes>self.filename.encode()
        #cdef Types.Particule_d part

        ##part = g.Double_Gadget_Read_format2(fname, &self.header, num_files, bpot, bacc, bdadt, bdt)
        #if part is NULL:
            #raise MemoryError

        #for i in range(6):
            #N += self.header.npart[i]

        #self.part = Types.FromPointer(part, N)

    def Read(self, format=1, bpot=False, bacc=False, bdadt=False, bdt=False):
        if format == 1:
            self._read_format1(bpot, bacc, bdadt, bdt)
        elif format == 2:
            self._read_format2(bpot, bacc, bdadt, bdt)

    def Write(self, format=1):
        if format == 1:
            self.Write = self._write_format1
        elif format == 2:
            self.Write = self._write_format2

    #property Part:
        #def __get__(self):
            #if self.part.ptr_data is not NULL:
                #return self.part
            #else:
                #return None
        #def __set__(self, value):
            #if isinstance(value, Types.Particules):
                #self.part = value
            #else:
                #raise TypeError("You must passed a InitialCond.Types.Particules!")

    property positions:
        def __get__(self):
            return self._pos
    property velocities:
        def __get__(self):
            return self._vel

    property npartTotalHighWord:
        @cython.boundscheck(False)
        def __get__(self):
            res = [0]*6
            for i in range(6):
                res[i] = self._header.npartTotalHighWord[i]
            return res
        @cython.boundscheck(False)
        def __set__(self, value):
            if len(value) != 6:
                raise ValueError("You should past a list of 6 integers!")
            for i in range(6):
                self._header.npartTotalHighWord[i] = value[i]

    property npart:
        @cython.boundscheck(False)
        def __get__(self):
            res = [0]*6
            for i in range(6):
                res[i] = self._header.npart[i]
            return res
        @cython.boundscheck(False)
        def __set__(self, value):
            if len(value) != 6:
                raise ValueError("You should past a list of 6 integers!")
            for i in range(6):
                self._header.npart[i] = value[i]

    property mass:
        @cython.boundscheck(False)
        def __get__(self):
            res = [0]*6
            for i in range(6):
                res[i] = self._header.mass[i]
            return res
        @cython.boundscheck(False)
        def __set__(self, value):
            if len(value) != 6:
                raise ValueError("You should past a list of 6 floats!")
            for i in range(6):
                self._header.mass[i] = value[i]

    property num_files:
        def __get__(self):
            return self._header.num_files
        def __set__(self, value):
            self._header.num_files = value

    property time:
        def __get__(self):
            return self._header.time
        def __set__(self, value):
            self._header.time = value

    property redshift:
        def __get__(self):
            return self._header.redshift
        def __set__(self, value):
            self._header.redshift = value

    property flag_sfr:
        def __get__(self):
            return self._header.flag_sfr
        def __set__(self, value):
            self._header.flag_sfr = value

    property flag_feedback:
        def __get__(self):
            return self._header.flag_feedback
        def __set__(self, value):
            self._header.flag_feedback = value

    property flag_cooling:
        def __get__(self):
            return self._header.flag_cooling
        def __set__(self, value):
            self._header.flag_cooling = value

    property BoxSize:
        def __get__(self):
            return self._header.BoxSize
        def __set__(self, value):
            self._header.BoxSize = value

    property Omega0:
        def __get__(self):
            return self._header.Omega0
        def __set__(self, value):
            self._header.Omega0 = value

    property OmegaLambda:
        def __get__(self):
            return self._header.OmegaLambda
        def __set__(self, value):
            self._header.OmegaLambda = value

    property HubbleParam:
        def __get__(self):
            return self._header.HubbleParam
        def __set__(self, value):
            self._header.HubbleParam = value

    property flag_stellarage:
        def __get__(self):
            return self._header.flag_stellarage
        def __set__(self, value):
            self._header.flag_stellarage = value

    property flag_metals:
        def __get__(self):
            return self._header.flag_metals
        def __set__(self, value):
            self._header.flag_metals = value

    property flag_entropy_instead_u:
        def __get__(self):
            return self._header.flag_entropy_instead_u
        def __set__(self, value):
            self._header.flag_entropy_instead_u = value

