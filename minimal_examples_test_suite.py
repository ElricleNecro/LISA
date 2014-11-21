#!/usr/bin/env python

from LISA.gui.sdl2.Figure import Figure

from LISA.examples.rippler import Rippler
from LISA.examples.heightmap import HeightMap
from LISA.examples.earth import Earth
from LISA.examples.sprite import Sprites

fig = Figure()
# fig.axes = Rippler()
# fig.axes = HeightMap()
# fig.axes = Earth()
fig.axes = Sprites()

input()
