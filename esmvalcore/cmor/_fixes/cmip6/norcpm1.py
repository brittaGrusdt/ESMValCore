"""Fixes for NorCPM1 model."""

from ..fix import Fix
from ..shared import round_coordinates


class AllVars(Fix):
    """Fixes for all variables."""

    def fix_metadata(self, cubes):
        """Fix metadata."""
        ensembles = ['r' + str(i) + 'i1p1f1' for i in range(1, 31)]
        for cube in cubes:
            if cube.attributes.get('variant_label', '') in ensembles:
                round_coordinates(
                    [cube],
                    decimals=3,
                    coord_names=['latitude'],
                )
        return cubes
