cdef extern from "cdistances.h":

    # function to compute the distance in periodic conditions
    double periodic_euclidean_distance(
        Point point_0,
        Point point,
        unsigned int dimension,
        void* extra
    )

    # function to compute the distance
    double euclidean_distance(
        Point point_0,
        Point point,
        unsigned int dimension,
        void* extra
    )

    # to compute the distance on the celestial sphere
    double haversine_sky_distance(
        Point point_0,
        Point point,
        unsigned int dimension,
        void* extra
    )

ctypedef double (*callback) (Point point_0, Point point, unsigned int dimension, void* extra)

cdef extern from "cBallTree.h":


    ctypedef struct Point:

        double* point
        unsigned long identity

    ctypedef struct Node:

        Point points
        Point center
        double radius

        unsigned int number
        unsigned int level

        Node parent
        Node child
        Node brother

    ctypedef struct BallTree:

        unsigned long npoints
        Point points
        Node root
        Node current
        callback distance
        void* extra

    BallTree BallTree_New(
        double* points,
        unsigned long* identities,
        unsigned long npoints,
        unsigned int dimension,
        unsigned int leaf_max,
        unsigned int level_max,
        callback distance,
        void* extra
    )

    void BallTree_search(
        BallTree tree,
        double* points_0,
        unsigned long npoints_0,
        double* radius,
        unsigned long*** identities,
        unsigned long** npoints
    )

    # find k nearest neighbors
    unsigned long* BallTree_k_nearest_neighbors(
        BallTree tree,
        double* points_0,
        unsigned long npoints_0,
        unsigned int k,
    )

    void BallTree_free(BallTree tree)
