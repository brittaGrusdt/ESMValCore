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
            if cube.attributes.get('variant_label', '') == 'r1i1p1f1':
                round_coordinates(
                    [cube],
                    decimals=3,
                    coord_names=['latitude'],
                )
        return cubes
