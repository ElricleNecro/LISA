#ifndef CDISTANCES_H_0DALN6K3
#define CDISTANCES_H_0DALN6K3

#include "cPoint.h"

// function to compute the distance in periodic conditions
double periodic_euclidean_distance(
    Point point_0,
    Point point,
    unsigned int dimension,
    void* extra
);

// function to compute the distance
double euclidean_distance(
    Point point_0,
    Point point,
    unsigned int dimension,
    void* extra
);

// to compute the distance on the celestial sphere
double haversine_sky_distance(
    Point point_0,
    Point point,
    unsigned int dimension,
    void* extra
);

#endif /* end of include guard: CDISTANCES_H_0DALN6K3 */

