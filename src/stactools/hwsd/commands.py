import logging
import os
from glob import glob

import click

from stactools.hwsd import cog, stac

logger = logging.getLogger(__name__)


def create_hwsd_command(cli):
    """Creates the stactools-hwsd command line utility."""
    @cli.group(
        "hwsd",
        short_help=("Commands for working with stactools-hwsd"),
    )
    def hwsd():
        pass

    @hwsd.command(
        "create-collection",
        short_help="Creates a STAC collection",
    )
    @click.option(
        "-d",
        "--destination",
        required=True,
        help="The output location for the STAC Collection.",
    )
    def create_collection_command(destination: str):
        """Creates a STAC Collection

        Args:
            destination (str): The output folder for the Collection.
        """
        collection = stac.create_collection()
        collection.normalize_hrefs(destination)
        collection.save(dest_href=destination)
        collection.validate()

        return None

    @hwsd.command("create-item", short_help="Create a STAC item")
    @click.option(
        "-s",
        "--source",
        required=True,
        help="The HREF for the location containing the data assets.",
    )
    @click.option(
        "-d",
        "--destination",
        required=True,
        help="An HREF for the STAC Collection.",
    )
    def create_item_command(source: str, destination: str):
        """Creates a STAC Item

        Args:
            source (str): HREF of the Assets associated with the Item
            destination (str): An HREF for the STAC Collection
        """
        item = stac.create_item(source)
        item.save_object(dest_href=destination)
        item.validate()

        return None

    @hwsd.command(
        "populate-collection",
        short_help="Populate the HWSD STAC Collection with all items",
    )
    @click.option(
        "-s",
        "--source",
        required=True,
        help="The source directory for the Item data assets.",
    )
    @click.option(
        "-d",
        "--destination",
        required=True,
        help="The output directory for the populated STAC Collection.",
    )
    def populate_collection_command(source: str, destination: str):
        """Populate the HWSD STAC Collection with all items

        Args:
            source (str): The source directory for the Item data assets
            destination (str): An HREF for the STAC Collection
        """

        collection = stac.create_collection()
        collection.normalize_hrefs(destination)
        collection.save(dest_href=destination)

        cog.create_cogs(source, destination)
        for cog_file in glob(f"{destination}/*.tif"):
            item = stac.create_item(cog_file)
            collection.add_item(item)
            item.set_self_href(cog_file.replace(".tif", ".json"))
            item.make_asset_hrefs_relative()
            item.save_object()

        collection.normalize_hrefs(destination)
        collection.save(dest_href=destination)
        collection.validate()

        return None

    @hwsd.command(
        "create-cog",
        short_help="Transform NetCDF to Cloud-Optimized Geotiff.",
    )
    @click.option(
        "-d",
        "--destination",
        required=True,
        help="The output directory for the COGs",
    )
    @click.option(
        "-s",
        "--source",
        required=True,
        help="The input NetCDF fle",
    )
    def create_cog_command(destination: str, source: str) -> None:
        """Generate a COG from a NetCDF.

        Args:
            destination (str): Local directory to save output COGs
            source (str): The input NetCDF file
        """
        if not os.path.isdir(destination):
            raise IOError(f'Destination folder "{destination}" not found')

        output_path = os.path.join(
            destination,
            os.path.basename(source).replace(".nc4", "") + ".tif")

        cog.create_cog(source, output_path)

    return hwsd
