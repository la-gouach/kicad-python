#  Copyright 2015 Piers Titus van der Torren
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
import math

nm = 0.000001
mm = 1.0
inch = 25.4
mil = 0.25400

nm_ius = 1
mm_ius = 1000000
inch_ius = 254000000
mil_ius = 25400

deg = 1.0
rad = 180.0 / math.pi

DEFAULT_UNIT_IUS = mm_ius


def inch_to_mm(val):
    """Convert from inch to mm.

    Handles single values, sequences, sequences of sequences, etc.
    """
    try:
        return val * 25.4
    except TypeError:
        return [inch_to_mm(v) for v in val]


def mm_to_inch(val):
    """Convert from mm to inch.

    Handles single values, sequences, sequences of sequences, etc.
    """
    try:
        return val / 25.4
    except TypeError:
        return [mm_to_inch(v) for v in val]


class BaseUnitTuple:
    """Base class to provide mm, inch, mil properties.

    It's a class to be used just by Point and Size.
    """
    @property
    def x(self):
        return float(self._wxobj.x) / DEFAULT_UNIT_IUS

    @x.setter
    def x(self, value):
        self._wxobj.x = value * DEFAULT_UNIT_IUS

    @property
    def y(self):
        return float(self._wxobj.y) / DEFAULT_UNIT_IUS

    @y.setter
    def y(self, value):
        self._wxobj.y = value * DEFAULT_UNIT_IUS

    def __getitem__(self, index):
        return self.mm[index]

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError

    def __sub__(self, b):
        return self._class(self._wxobj - b._wxobj)

    def __add__(self, b):
        return self._class(self._wxobj + b._wxobj)

    def __eq__(self, other):
        return (self._wxobj == other._wxobj)

    def __ne__(self, other):
        return not (self == other)

    def __len__(self):
        return len(self._wxobj)

    def _unit_tuple(self, unit_multiplier):
        unit_multiplier_float = float(unit_multiplier)
        return (self.x / unit_multiplier_float,
                self.y / unit_multiplier_float)

    @property
    def nm(self):
        return self._unit_tuple(nm)

    @property
    def mm(self):
        """Get the milimeters tuple."""
        return (self.x, self.y)

    @property
    def inch(self):
        """Get the inches tuple."""
        return self._unit_tuple(inch)

    @property
    def mil(self):
        """Get the mils tuple."""
        return self._unit_tuple(mil)

    @staticmethod
    def _tuple_to_class(v, cls):
        if type(v) == cls:
            return v
        elif type(v) == tuple:
            if len(v) != 2:
                raise TypeError("A point parameter must be a 2 value tuple")
        return cls(v[0], v[1])