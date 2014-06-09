#ifndef BALLTREE_H
#define BALLTREE_H

#define _XOPEN_SOURCE
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <math.h>

typedef struct _BallTree* BallTree;

#include "cPoint.h"
#include "cNode.h"

#define min( a, b ) ( ( (a) < (b) ) ? (a) : (b) )
#define max( a, b ) ( ( (a) < (b) ) ? (b) : (a) )
#define M_2PI 2. * M_PI

// The structure for the quadtree
struct _BallTree {

    // number of points
    unsigned long npoints;

    // Points
    Point points;

    // the dimension of the space in which we are computing
    unsigned int dimensions;

    // Arrays for storing the searched points
    unsigned long* work;
    unsigned long wdim;
    unsigned long current_wdim;

    // A temporary array for centroid computation
    double* center;

    // the parameters of the tree
    unsigned long leaf_max;
    unsigned long level_max;

    // compute the separation between two points
    double (*distance)(
        Point point_0,
        Point point,
        unsigned int dimension,
        void* extra
    );

    // a pointer to pass data to the distance function for extra arguments
    void* extra_distance;

    // the root of the quadtree
    Node root;

    // the current node
    Node current;

};

// to create a new quadtree
BallTree BallTree_New(
    double* points,
    unsigned long* identities,
    unsigned long npoints,
    unsigned int dimensions,
    unsigned int leaf_max,
    unsigned int level_max,
    double (*distance)(
        Point point_0,
        Point point,
        unsigned int dimension,
        void* extra
    ),
    void* extra_distance
);

// create the quadtree
void BallTree_create(
    BallTree tree
);

// free the tree
void BallTree_free(BallTree tree);

// check the quadtree
bool BallTree_check(BallTree tree);

// search points around points
void BallTree_search(
    BallTree tree,
    double* points_0,
    unsigned long npoints_0,
    double* radius,
    unsigned long*** identities,
    unsigned long** npoints
);

// find k nearest neighbors
unsigned long* BallTree_k_nearest_neighbors(
    BallTree tree,
    double* points_0,
    unsigned long npoints_0,
    unsigned int k
);

// increase workspace for searching points
void BallTree_set_workspace(
    BallTree tree,
    unsigned long wdim
);

// search points inside the area in node and append them to list
void BallTree_appendInRadius(
    BallTree tree,
    Node node,
    Node query
);

// append points to the list of points in the area
void BallTree_appendPoints(
    BallTree tree,
    Point points,
    unsigned long npoints
);

#endif /* end of include guard */
