#ifndef CNODE_H_N20DFEIC
#define CNODE_H_N20DFEIC

#include <stdio.h>

typedef struct _Node* Node;

#include "cPoint.h"
#include "cBallTree.h"
#include "cQueue.h"

// Define a node for the quadtree
struct _Node {

    // Points in the node
    Point points;

    // The associated box to the node
    Point center;
    double radius;

    // Number of points in the node
    unsigned int number;

    // level
    unsigned int level;

    // the dimension with the maximal spread
    unsigned int dimension;

    // A link to the parent
    struct _Node* parent;

    // A link to the child
    struct _Node* child;

    // A link to the brother
    struct _Node* brother;

};

// to create a node
Node Node_New(void);

// find node of a point
Node Point_find_node(
    Point point,
    Node root
);

// set property of node from parent
void Node_from_parent_node(
    Node node,
    Node parent,
    unsigned int number
);

// to subdivide points in child nodes
void Node_subdivide(
    BallTree tree,
    Node node
);

// free a node recursively
void Node_free(Node root);

// to display the tree
void Node_all(Node node, FILE* f);

// set corners
void Node_set_corners(Node node);

// compute the centroid of a point
void Node_compute_centroid(
    BallTree tree,
    Node node
);

// compute radius
void Node_compute_radius(
    BallTree tree,
    Node node
);

// dimension with maximal spread
void Node_spread_dimension(
    BallTree tree,
    Node node
);

// split a node
void Node_split(
    BallTree tree,
    Node node
);

// Create a child node
void Node_child(
    Node* node,
    Node parent,
    Point points,
    unsigned long nmax
);

// used to compare in nodes
int Comparison(
    const void* a,
    const void* b
);

// say if node and area intersect
bool Node_intersect(
    BallTree tree,
    Node node,
    Node query
);

// recursively build node
void Node_build(
    BallTree tree,
    Node parent
);

// count in leaf
void Node_count_in_leaf(
    Node root,
    unsigned long* count
);

// check if a point is in a node
bool Node_is_in(
    Node node,
    Point point
);

// check if a node is at given distance from a central point
bool Node_in_radius(
    Node node,
    Point point_0,
    double radius
);

// check if a node is ENTIRELY at a given distance from central point
bool Node_all_in_radius(
    BallTree tree,
    Node node,
    Node query
);

// search in a cone around a point in node
void Node_search(
    BallTree tree,
    Node node,
    Node query
);

// search fr neighbors
void Node_search_neighbors(
    BallTree tree,
    Node node,
    Node query,
    Queue queue
);


#endif /* end of include guard: CNODE_H_N20DFEIC */

