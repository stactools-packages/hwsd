import logging
import os

import click
from stactools.core.utils.convert import cogify

from stactools.hwsd import stac

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

    @hwsd.command("populate-collection",
                  short_help="Populate the HWSD STAC Collection with all items"
                  )
    @click.option("-s",
                  "--source",
                  required=True,
                  help="The source directory for the Item data assets.")
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

        item = stac.create_item(source)
        collection.add_item(item)

        collection.normalize_hrefs(destination)
        collection.save(dest_href=destination)
        collection.validate()

        return None

    @hwsd.command(
        "create-cog",
        short_help="Transform Geotiff to Cloud-Optimized Geotiff.",
    )
    @click.option("-d",
                  "--destination",
                  required=True,
                  help="The output directory for the COG")
    @click.option("-s",
                  "--source",
                  required=True,
                  help="Path to an input GeoTiff")
    def create_cog_command(destination: str, source: str) -> None:
        """Generate a COG from a GeoTiff. The COG will be saved in the desination
        with `_cog.tif` appended to the name.

        Args:
            destination (str): Local directory to save output COGs
            source (str): A GeoTIFF
        """
        if not os.path.isdir(destination):
            raise IOError(f'Destination folder "{destination}" not found')

        output_path = os.path.join(destination,
                                   os.path.basename(source)[:-4] + "_cog.tif")

        args = ["-co", "OVERVIEWS=IGNORE_EXISTING"]

        cogify(source, output_path, args)

    return hwsd
