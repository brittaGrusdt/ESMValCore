"""Fixes for CESM2-WACCM-FV2 model."""
from .cesm2 import Tas as BaseTas
from .cesm2 import Fgco2 as BaseFgco2
from .cesm2 import Omon as BaseOmon
from .cesm2_waccm import Cl as BaseCl
from .cesm2_waccm import Cli as BaseCli
from .cesm2_waccm import Clw as BaseClw
from ..common import SiconcFixScalarCoord
from ..fix import Fix

import iris

class Msftmz(Fix):
    """Fixes for discrete DimCoord, code taken from: https://github.com/ESMValGroup/ESMValCore/compare/main...dhohn:fix_datasets_amoc?expand=1#:~:text=class%20Msftmz(,super().fix_metadata(cubes)"""

    @staticmethod
    def transform_region_coord(coord: iris.coords.DimCoord) -> iris.coords.AuxCoord:
        """transform a DimCoord with indexes as points to AuxCoord with names as points
        Parameters
        ----------
        coord: iris.coords.DimCoord
        Returns
        -------
        iris.coords.AuxCoord
        
        """
        # parses string like: 'atlantic_arctic_ocean=0, indian_pacific_ocean=1, global_ocean=2'
        lookup = { int(p[1]):p[0] for p in map(lambda x: x.split("="), coord.attributes['requested'].split(",")) }
        new_points = ['']*len(lookup)
        for old_label in coord.points:
            new_points[old_label] = lookup[old_label]
        new_coord = iris.coords.AuxCoord(new_points, 
                                         standard_name="region", 
                                         var_name="basin", 
                                         long_name="ocean basin",
                                         units="no unit")
        return new_coord

    def fix_metadata(self, cubes):
        """Fix for region DimCoord with indexes as points
        to AuxCoord with names as points
        Parameters
        ----------
        cubes: iris CubeList
            List of cubes to fix
        Returns
        -------
        iris.cube.CubeList
        """
        cube = self.get_cube_from_list(cubes)
        coord = cube.coord("region")
        new_coord = self.transform_region_coord(coord=coord)
        dims = cube.coord_dims("region")
        for cube in cubes:
            cube.remove_coord("region")
            cube.add_aux_coord(new_coord, dims)
        return cubes
        # return super().fix_metadata(cubes)

Cl = BaseCl


Cli = BaseCli


Clw = BaseClw


Fgco2 = BaseFgco2


Omon = BaseOmon


Siconc = SiconcFixScalarCoord


Tas = BaseTas
