# class to make a mesh on celestial sphere
# and then to do searches on it easily

cimport BallTree as CQT
cimport numpy as np
import numpy as np
import tempfile

from matplotlib.patches import Rectangle
from stdlib cimport free


EPS = np.finfo(np.float64).eps * 10


cdef CQT.callback _get_metric(metric):
    if metric == "euclidean":
        return CQT.euclidean_distance
    elif metric == "periodic_euclidean":
        return CQT.periodic_euclidean_distance
    elif metric == "haversine_sky":
        return CQT.haversine_sky_distance


cdef class Balltree(object):

    """
    A class to handle a celestial mesh to
    do fast points search in the mesh and
    in the celestial sphere.
    The underlying code is written in C
    and wrapped by Cython to use in Python way.
    """

    cdef CQT.BallTree tree

    def __init__(
        self,
        points,
        identities,
        leaf_max=15,
        level_max=100,
        metric="euclidean",
        extra=np.array([], dtype=np.double),
    ):

        """
        Initialization of the celestial mesh
        with the coordinates in RA, DEC and the
        identities of points to retrieve them.
        Needs to specify roughly the angular size
        of boxes in the mesh in RA, DEC directions.
        """

        cdef :
            np.ndarray[np.double_t, ndim=2, mode="c"] points_np = \
                np.asarray(points, dtype=np.double)
            np.ndarray[np.uint64_t, ndim=1, mode="c"] identities_np = \
                np.asarray(identities, dtype=np.uint64)
            np.ndarray[np.double_t, ndim=1, mode="c"] extra_np = \
                np.asarray(extra, dtype=np.double)
            CQT.callback function

        # create a new object of mesh
        function = _get_metric(metric)
        self.tree = CQT.BallTree_New(
            <double*>points_np.data,
            <unsigned long*>identities_np.data,
            <unsigned long>points_np.shape[0],
            <unsigned long>points_np.shape[1],
            <unsigned int>leaf_max,
            <unsigned int>level_max,
            function,
            <double*>extra_np.data,
        )

    def get_neighbors(self, points_0, radius):

        """
        Method which returns the identities of points
        in the celestial mesh around a point with
        celestial coordinates specified in argument
        with an angular separation in argument.
        """

        cdef :
            unsigned long** identities
            unsigned long[:] tmp_ids
            unsigned long* npoints

            np.ndarray[np.double_t, ndim=2, mode="c"] points_np = \
                np.asarray(points_0, dtype=np.double)
            np.ndarray[np.double_t, ndim=1, mode="c"] radius_np = \
                np.asarray(radius, dtype=np.double)

        # get result
        CQT.BallTree_search(
            self.tree,
            <double*>points_np.data,
            <unsigned long>points_np.shape[0],
            <double*>radius_np.data,
            &identities,
            &npoints
        )

        # pythonize result
        tmp = np.asarray(
            [np.asarray(
                <unsigned long[:npoints[i]]> identities[i],
                dtype=np.int64,
            ) for i in range(points_np.shape[0])],
            dtype=np.object,
        )

        # free the memory
        for j in range(points_np.shape[0]):
            free(identities[j])
        free(identities)
        free(npoints)

        return tmp

    def get_nearest_neighbors(self, points, k):

        """
        Method which returns the identities of points
        in the celestial mesh around a point with
        celestial coordinates specified in argument
        with an angular separation in argument.
        """

        cdef :
            unsigned long* identities
            unsigned long j

            np.ndarray[np.double_t, ndim=2, mode="c"] points_np = \
                np.asarray(points, dtype=np.double)

        # get nearest neighbors from c
        identities = CQT.BallTree_k_nearest_neighbors(
            self.tree,
            <double*>points_np.data,
            <unsigned long>points_np.shape[0],
            <unsigned int> k
        )

        # store the result
        tmp = np.asarray(
            <unsigned long[:points_np.shape[0], :k]> identities,
            dtype = np.int64,
        )

        return tmp

    def __dealloc__(self):

        CQT.BallTree_free(self.tree)
