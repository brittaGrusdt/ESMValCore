"""Fixes for EC-Earth3 model."""
import cf_units
import numpy as np

from ..fix import Fix
from ..shared import round_coordinates


class AllVars(Fix):
    """Fixes for all variables."""

    def fix_metadata(self, cubes):
        """Fix metadata."""
        for cube in cubes:
            if cube.attributes.get('variant_label', '') == 'r1i1p4f1':
                round_coordinates(
                    [cube],
                    decimals=3,
                    coord_names=['latitude'],
                )
                if (cube.attributes.get('experiment_id', '') == 'historical'
                        and cube.coords('time')):
                    time_coord = cube.coord('time')
                    time_coord.units = cf_units.Unit(time_coord.units.origin,
                                                     'proleptic_gregorian')
        return cubes
