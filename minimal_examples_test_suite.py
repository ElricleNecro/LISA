#!/usr/bin/env python

import argparse
from LISA.gui.sdl2.Figure import Figure

from LISA.examples.rippler import Rippler
from LISA.examples.heightmap import HeightMap
from LISA.examples.earth import Earth
from LISA.examples.earth_lighting import Earth as EarthLight
from LISA.examples.sprite import Sprites
from LISA.examples.sphere_refinement import SphereRefinement

# read arguments
parser = argparse.ArgumentParser(
    description="To run easily various examples."
)

# commands
parser.add_argument(
    '--Rippler',
    help="Plot the example of the rippler",
    action="store_true",
    default=False,
)
parser.add_argument(
    '--Earth',
    help="Plot the example of the earth",
    action="store_true",
    default=False,
)
parser.add_argument(
    '--HeightMap',
    help="Plot the example of the heightmap",
    action="store_true",
    default=False,
)
parser.add_argument(
    '--Sprites',
    help="Plot the example of the sprites",
    action="store_true",
    default=False,
)
parser.add_argument(
    '--EarthLight',
    help="Plot the example of the earth with widget controls",
    action="store_true",
    default=False,
)
parser.add_argument(
    '--SphereRefinement',
    help="Plot the example of the mesh sphere with refinement",
    action="store_true",
    default=False,
)

# parse command line
args = parser.parse_args()

# create a figure
fig = Figure()

# loop over keys
for key, value in args.__dict__.items():
    if value:
        fig.axes = locals()[key]()

input()
