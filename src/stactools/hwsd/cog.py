import logging
import os
from glob import glob
from subprocess import CalledProcessError, check_output

# import rasterio
from stactools.hwsd.constants import DATA_TYPES, NO_DATA
from stactools.hwsd.stac import asset_name_from_href

logger = logging.getLogger(__name__)


def create_cogs(
    input_directory: str,
    output_directory: str,
) -> None:
    """Create COG from a NetCDF file

    Args:
        input_directory (str): The directory containing NetCDF files.
        output_directory (str): The directory to which the COGs will be written.

    Returns:
        None
    """

    for in_file in glob(f"{input_directory}/*.nc4"):
        if os.path.basename(in_file) != "HWSD_SOIL_CLM_RES.nc4":
            out_file = os.path.join(output_directory,
                                    f"{asset_name_from_href(in_file)}.tif")
            create_cog(in_file, out_file)


def create_cog(
    input_path: str,
    output_path: str,
) -> None:
    """Create COG from a NetCDF file

    Args:
        input_path (str): Path to a NetCDF file.
        output_path (str): The path to which the COG will be written.

    Returns:
        None
    """

    output = None
    try:
        logger.info("Converting NetCDF to COG")
        logger.debug(f"input_path: {input_path}")
        logger.debug(f"output_path: {output_path}")
        cmd = [
            "gdal_translate",
            "-ot",
            DATA_TYPES[asset_name_from_href(output_path)].value,
            # "-strict",
            # "-unscale",
            # "-scale",
            # "-1", "7", "-1", "7",
            "-of",
            "COG",
            "-co",
            "NUM_THREADS=ALL_CPUS",
            "-co",
            "BLOCKSIZE=512",
            "-co",
            "COMPRESS=DEFLATE",
            "-co",
            "LEVEL=9",
            "-co",
            "PREDICTOR=YES",
            "-co",
            "OVERVIEWS=IGNORE_EXISTING",
            "-a_nodata",
            str(NO_DATA),
            input_path,
            output_path,
        ]

        try:
            output = check_output(cmd)
        except CalledProcessError as e:
            output = e.output
            raise
        finally:
            logger.info(f"output: {str(output)}")
        # with rasterio.open(output_path, "r+") as dataset:
        # #     dataset.write_colormap(1, COLOUR_MAP)

        #     data = dataset.read(1)

        #     dt = rasterio.dtypes.get_minimum_dtype(data)
        #     print(dt)
        #     print(rasterio.dtypes.can_cast_dtype(data, "float32"))
        #     print(rasterio.dtypes.can_cast_dtype(data, "int16"))
        #     print(rasterio.dtypes.can_cast_dtype(data, "byte"))
        #     print(data)

    except Exception:
        logger.error("Failed to process {}".format(output_path))
        raise
