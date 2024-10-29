"""Fixes for CESM2-WACCM model."""

from netCDF4 import Dataset

from ..common import SiconcFixScalarCoord
from .cesm2 import Cl as BaseCl
from .cesm2 import Fgco2 as BaseFgco2
from .cesm2 import Omon as BaseOmon
from .cesm2 import Tas as BaseTas
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

class Cl(BaseCl):
    """Fixes for cl."""

    def fix_file(self, filepath, output_dir, add_unique_suffix=False):
        """Fix hybrid pressure coordinate.

        Adds missing ``formula_terms`` attribute to file.

        Note
        ----
        Fixing this with :mod:`iris` in ``fix_metadata`` or ``fix_data`` is
        **not** possible, since the bounds of the vertical coordinates ``a``
        and ``b`` are not present in the loaded :class:`iris.cube.CubeList`,
        even when :func:`iris.load_raw` is used.

        Parameters
        ----------
        filepath : str
            Path to the original file.
        output_dir: Path
            Output directory for fixed files.
        add_unique_suffix: bool, optional (default: False)
            Adds a unique suffix to `output_dir` for thread safety.

        Returns
        -------
        str
            Path to the fixed file.

        """
        new_path = self._fix_formula_terms(
            filepath, output_dir, add_unique_suffix=add_unique_suffix
        )
        dataset = Dataset(new_path, mode="a")
        dataset.variables["a_bnds"][:] = dataset.variables["a_bnds"][:, ::-1]
        dataset.variables["b_bnds"][:] = dataset.variables["b_bnds"][:, ::-1]
        dataset.close()
        return new_path


Cli = Cl


Clw = Cl


Fgco2 = BaseFgco2


Omon = BaseOmon


Siconc = SiconcFixScalarCoord


Tas = BaseTas
