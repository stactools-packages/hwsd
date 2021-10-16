import logging
import os
from typing import Any, List

from pystac import (CatalogType, Collection, Extent, MediaType, SpatialExtent,
                    TemporalExtent)
from pystac.asset import Asset
from pystac.extensions.item_assets import AssetDefinition, ItemAssetsExtension
from pystac.extensions.projection import (ProjectionExtension,
                                          SummariesProjectionExtension)
from pystac.extensions.raster import RasterBand, RasterExtension
from pystac.extensions.scientific import ScientificExtension
from pystac.item import Item
from pystac.link import Link
from pystac.rel_type import RelType
from pystac.utils import str_to_datetime
from shapely.geometry.geo import box

from stactools.hwsd.constants import (ASSETS_METADATA, CITATION, DESCRIPTION,
                                      DOCUMENTATION, DOI, EPSG, HOMEPAGE_1,
                                      HOMEPAGE_2, HOMEPAGE_REGRIDDED, ID,
                                      KEYWORDS, LICENSE, LICENSE_LINK, NODATA,
                                      PROVIDERS, SPATIAL_EXTENT,
                                      TEMPORAL_EXTENT, THUMBNAIL, TITLE)

logger = logging.getLogger(__name__)


def create_collection() -> Collection:
    """Create a STAC Collection
    Create a STAC Collection for the HWSD.

    Returns:
        Collection: STAC Collection object
    """

    temporal_extent: List[Any] = [
        str_to_datetime(dt) if dt is not None else None
        for dt in TEMPORAL_EXTENT
    ]
    extent = Extent(
        SpatialExtent([SPATIAL_EXTENT]),
        TemporalExtent(temporal_extent),
    )

    collection = Collection(
        id=ID,
        title=TITLE,
        description=DESCRIPTION,
        keywords=KEYWORDS,
        license=LICENSE,
        providers=PROVIDERS,
        extent=extent,
        catalog_type=CatalogType.RELATIVE_PUBLISHED,
    )

    collection.add_link(LICENSE_LINK)
    collection.add_link(Link(RelType.VIA, target=HOMEPAGE_1, title="Homepage"))
    collection.add_link(
        Link(RelType.VIA, target=HOMEPAGE_2, title="Homepage, Alternate"))
    collection.add_link(
        Link(RelType.VIA,
             target=HOMEPAGE_REGRIDDED,
             title="Homepage, Regridded"))

    proj_ext = SummariesProjectionExtension(collection)
    proj_ext.epsg = [EPSG]

    sci_ext = ScientificExtension.ext(collection, add_if_missing=True)
    sci_ext.doi = DOI
    sci_ext.citation = CITATION

    collection.add_asset(
        "documentation",
        Asset(media_type="application/pdf",
              roles=["metadata"],
              title="Documentation",
              href=DOCUMENTATION))

    collection.add_asset(
        "thumbnail",
        Asset(media_type=MediaType.PNG,
              roles=["thumbnail"],
              title="Thumbnail",
              href=THUMBNAIL))

    item_asset_ext = ItemAssetsExtension.ext(collection, add_if_missing=True)
    asset_names = list(ASSETS_METADATA["Description"].keys())
    item_assets = {
        a: AssetDefinition({
            "types": [MediaType.COG],
            "roles": ["data"],
            "title": a,
            "proj:epsg": EPSG
        })
        for a in asset_names
    }
    item_assets["Documentation"] = AssetDefinition({
        "types": ["application/pdf"],
        "roles": ["metadata"],
        "title": "Documentation",
    })
    item_asset_ext.item_assets = item_assets

    return collection


def create_item(assets_location: str) -> Item:
    """Create a STAC Item
    Create a STAC Item for one year of the HWSD. The asset_href should include
     the observation year as the first part of the filename.

    Args:
        assets_location (str): The HREF pointing to the location containing all item data assets

    Returns:
        Item: STAC Item object
    """

    polygon = box(*SPATIAL_EXTENT, ccw=True)
    coordinates = [list(i) for i in list(polygon.exterior.coords)]
    geometry = {"type": "Polygon", "coordinates": [coordinates]}

    properties = {
        "title": TITLE,
        "description": DESCRIPTION,
        "start_datetime": TEMPORAL_EXTENT[0],
        "end_datetime": TEMPORAL_EXTENT[1],
    }

    item = Item(
        id=ID,
        geometry=geometry,
        bbox=SPATIAL_EXTENT,
        datetime=str_to_datetime(TEMPORAL_EXTENT[0]),
        properties=properties,
    )

    item.add_link(Link(RelType.VIA, target=HOMEPAGE_1, title="Homepage"))
    item.add_link(
        Link(RelType.VIA, target=HOMEPAGE_2, title="Homepage, Alternate"))
    item.add_link(
        Link(RelType.VIA,
             target=HOMEPAGE_REGRIDDED,
             title="Homepage, Regridded"))

    sci_ext = ScientificExtension.ext(item, add_if_missing=True)
    sci_ext.citation = CITATION
    sci_ext.doi = DOI

    proj_attrs = ProjectionExtension.ext(item, add_if_missing=True)
    proj_attrs.epsg = EPSG

    item.add_asset(
        "documentation",
        Asset(media_type="application/pdf",
              roles=["metadata"],
              title="HWSD Documentation",
              href=DOCUMENTATION))

    asset_names = list(ASSETS_METADATA["Description"].keys())
    for asset_name in asset_names:
        data_asset = Asset(
            href=os.path.join(assets_location, f"{asset_name}.nc4"),
            media_type=MediaType.COG,
            roles=["data"],
            title=asset_name,
            description=ASSETS_METADATA["Description"][asset_name],
            extra_fields={
                "units": ASSETS_METADATA["Units"][asset_name],
                "notes": ASSETS_METADATA["Notes"][asset_name],
            })
        item.add_asset(asset_name, data_asset)

        # Include raster information
        sampling: Any = "area"
        rast_band = RasterBand.create(nodata=NODATA, sampling=sampling)
        rast_ext = RasterExtension.ext(data_asset, add_if_missing=True)
        rast_ext.bands = [rast_band]

    return item
