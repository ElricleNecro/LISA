#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np


class Sphere(object):
    """
    A mesh of a sphere with different levels of refinement possible.
    """

    def __init__(self, center, observer):
        """
        Store some informations of the sphere on the 3D space.
        """
        self.center = center
        self.observer = observer

    def __call__(self):
        """
        Creates a sphere with the specified level of refinements.
        """
        # initialize the triangles
        self.initialize()

        # list of triangles to remove and to append
        triangles = []

        # loop over existing triangles
        for triangle in self.triangles:
            # subdivide if necessary
            triangles += self._subdivide(triangle)

        # append new ones
        self.triangles = triangles

    def _subdivide(self, triangle):
        """
        To subdivide a triangle into four other triangles.
        """
        # list of triangles
        triangles = []

        # check that we can subdivide it according to the solid angle criteria
        if self.solidAngle(triangle) > 0.005:
            # get the middle points
            a = self.getMiddlePoint(triangle[0], triangle[1])
            b = self.getMiddlePoint(triangle[1], triangle[2])
            c = self.getMiddlePoint(triangle[2], triangle[0])

            # subdivide the other triangles
            triangles += self._subdivide([triangle[0], a, c])
            triangles += self._subdivide([triangle[1], b, a])
            triangles += self._subdivide([triangle[2], c, b])
            triangles += self._subdivide([a, b, c])

        # else add simply to the other triangle
        else:
            triangles.append(triangle)

        # return the triangles
        return triangles

    def _toWorldSpace(self, point):
        """
        Put the point into the world space coordinates.
        """
        return [
            point[0] + self.center[0] - self.observer[0],
            point[1] + self.center[1] - self.observer[1],
            point[2] + self.center[2] - self.observer[2],
        ]

    @staticmethod
    def _determinant(a, b, c):
        """
        Gives the matrix determinant for the matrix composed of the three
        vectors that are the position of the triangle.
        """

        return abs(a[0] * (b[1] * c[2] - c[1] * b[2]) - a[1] * (
            b[0] * c[2] - c[0] * b[2]
        ) + a[2] * (b[0] * c[1] - c[0] * b[1]))

    def _dotProduct(self, a, b):
        """
        Compute the dot product between two points.
        """
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

    def solidAngle(self, triangle):
        """
        Computes the solid angle of a triangle from the point of view of the
        observer.
        """

        # get points of the triangle in the good coordinates
        pointa = self._toWorldSpace(self.positions[triangle[0]])
        pointb = self._toWorldSpace(self.positions[triangle[1]])
        pointc = self._toWorldSpace(self.positions[triangle[2]])

        # compute the determinant
        det = self._determinant(pointa, pointb, pointc)

        # the tangent
        det = det / (
            1. +
            self._dotProduct(pointa, pointb) +
            self._dotProduct(pointa, pointc) +
            self._dotProduct(pointb, pointc)
        )
        return float(2. * np.arctan(det))

    def addVertex(self, point):
        """
        To add a vertex to the list of points available.
        """

        # normalize the point
        length = np.sqrt(
            point[0] * point[0] + point[1] * point[1] + point[2] * point[2]
        )

        # append the position to the list of vertices
        self.positions.append(
            [point[0] / length, point[1] / length, point[2] / length]
        )

        # increment the number
        index = self.index
        self.index += 1
        return index

    def getMiddlePoint(self, p1, p2):
        """
        Given the indices of two points, returns the point that is the middle
        of the segment and normalize it to unit sphere. Uses the points cache
        if the point is already present.
        """

        # check if the first index is smaller
        firstSmaller = p1 < p2

        # get the indices
        smallerIndex = p1 if firstSmaller else p2
        greaterIndex = p2 if firstSmaller else p1

        # the key for the cache of middle points
        key = (smallerIndex, greaterIndex)

        # return the cache if present
        if key in self.cache:
            return self.cache[key]

        # not in cache so we compute the middle
        point1 = self.positions[p1]
        point2 = self.positions[p2]
        middle = [
            (point1[0] + point2[0]) * 0.5,
            (point1[1] + point2[1]) * 0.5,
            (point1[2] + point2[2]) * 0.5,
        ]

        # add the middle in the list of vertices
        index = self.addVertex(middle)

        # add the middle point in the cache
        self.cache[key] = index

        # return the index
        return index


class IcoSphere(Sphere):
    """
    Generates a spherical mesh with an iscocahedron bases for the refinement.
    """

    def initialize(self):
        """
        Gives the initial positions and triangles of the spherical mesh.
        """

        # the index of number of vertices
        self.index = 0

        # list of positions
        self.positions = []

        # list of triangles
        self.triangles = []

        # a cache for middle points
        self.cache = {}

        # create 12 vertices of the isocahedron
        t = 0.5 * (1. + np.sqrt(5.))
        self.addVertex([-1., t, 0.])
        self.addVertex([1., t, 0.])
        self.addVertex([-1., -t, 0.])
        self.addVertex([1., -t, 0.])

        self.addVertex([0., -1., t])
        self.addVertex([0., 1., t])
        self.addVertex([0., -1., -t])
        self.addVertex([0., 1., -t])

        self.addVertex([t, 0., -1.])
        self.addVertex([t, 0., 1.])
        self.addVertex([-t, 0., -1.])
        self.addVertex([-t, 0., 1.])

        # create 20 faces of the isocahedron
        self.triangles.append([0, 11, 5])
        self.triangles.append([0, 5, 1])
        self.triangles.append([0, 1, 7])
        self.triangles.append([0, 7, 10])
        self.triangles.append([0, 10, 11])

        self.triangles.append([1, 5, 9])
        self.triangles.append([5, 11, 4])
        self.triangles.append([11, 10, 2])
        self.triangles.append([10, 7, 6])
        self.triangles.append([7, 1, 8])

        self.triangles.append([3, 9, 4])
        self.triangles.append([3, 4, 2])
        self.triangles.append([3, 2, 6])
        self.triangles.append([3, 6, 8])
        self.triangles.append([3, 8, 9])

        self.triangles.append([4, 9, 5])
        self.triangles.append([2, 4, 11])
        self.triangles.append([6, 2, 10])
        self.triangles.append([8, 6, 7])
        self.triangles.append([9, 8, 1])

# vim: set tw=79 :
