"""Fixes for EC-Earth3-Veg-LR model."""

from ..common import OceanFixGrid
from ..fix import Fix

Siconc = OceanFixGrid


class Tos(Fix):
    def fix_metadata(self, cubes):
        """Fix metadata."""

        dim1 = "cell index along first dimension"
        dim2 = "cell index along second dimension"
        for cube in cubes:
            if cube.attributes.get("variant_label", "") == "r2i1p1f1":
                cube.dim_coords[1].rename(dim2)
                cube.dim_coords[2].rename(dim1)

        return cubes
