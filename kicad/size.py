#  Copyright 2015 Miguel Angel Ajo Pelayo <miguelangel@ajo.es>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

#TODO(mangelajo): we will have to come with something more generic
#                 or make the wx* objects compatible across bindings
pcbnew = __import__('pcbnew')
from kicad.units import *


class Size(BaseUnitTuple):

    def __init__(self, *args):
        self._class = Size
        if len(args) == 2:
            x, y = args
            self._wxobj = pcbnew.wxSize(x * units.DEFAULT_UNIT_IUS,
                                        y * units.DEFAULT_UNIT_IUS)
        else:
            self._wxobj = args[0]

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Size(%g, %g)" % self.mm

    def scale(self, x, y):
        """Scale this size by x horizontally, and y vertically."""
        scaled = self.scaled(x, y)
        self.x = scaled.x
        self.y = scaled.y

    def scaled(self, x, y):
        """Return a new scaled point, scaling by x and y."""
        scaled = self.Scale(x, y)
        return Size(scaled.x, scaled.y)

    @property
    def width(self):
        """Return the width of the size."""
        return self.x

    @width.setter
    def width(self, value):
        """Set the width of the size."""
        self.x = value

    @property
    def height(self):
        """Return the height of the size."""
        return self.y

    @height.setter
    def height(self, value):
        """Set the height of the size."""
        self.y = value