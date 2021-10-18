import logging
import os
from typing import Any, Dict, List, Optional

from pystac import (
    CatalogType,
    Collection,
    Extent,
    MediaType,
    SpatialExtent,
    TemporalExtent,
)
from pystac.asset import Asset
from pystac.extensions.item_assets import AssetDefinition, ItemAssetsExtension
from pystac.extensions.projection import (
    ProjectionExtension,
    SummariesProjectionExtension,
)
from pystac.extensions.raster import RasterBand, RasterExtension, Sampling
from pystac.extensions.scientific import ScientificExtension
from pystac.item import Item
from pystac.link import Link
from pystac.rel_type import RelType
from pystac.utils import str_to_datetime
from shapely.geometry.geo import box
from stactools.core.io import ReadHrefModifier

from stactools.hwsd.constants import (
    ASSET_DATA_TYPES,
    ASSET_DESCRIPTIONS,
    ASSET_NOTES,
    ASSET_UNITS,
    CITATION,
    DESCRIPTION,
    DOCUMENTATION,
    DOI,
    EPSG,
    HOMEPAGE_1,
    HOMEPAGE_2,
    HOMEPAGE_REGRIDDED,
    HWSD_CRS,
    ID,
    KEYWORDS,
    LICENSE,
    LICENSE_LINK,
    NO_DATA,
    PROVIDERS,
    SHAPE,
    SPATIAL_EXTENT,
    TEMPORAL_EXTENT,
    THUMBNAIL,
    TITLE,
    TRANSFORM,
)

logger = logging.getLogger(__name__)


def asset_name_from_href(href):
    return os.path.basename(href).replace(".nc4", "").replace(".tif", "")


def get_geometry() -> Dict[str, Any]:
    polygon = box(*SPATIAL_EXTENT, ccw=True)
    coordinates = [list(i) for i in list(polygon.exterior.coords)]
    return {"type": "Polygon", "coordinates": [coordinates]}


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
        Asset(
            media_type="application/pdf",
            roles=["metadata"],
            title="Documentation",
            href=DOCUMENTATION,
        ))

    collection.add_asset(
        "thumbnail",
        Asset(
            media_type=MediaType.PNG,
            roles=["thumbnail"],
            title="Thumbnail",
            href=THUMBNAIL,
        ))

    item_assets_ext = ItemAssetsExtension.ext(collection, add_if_missing=True)
    item_assets_ext.item_assets = {
        "data":
        AssetDefinition({
            "types": MediaType.COG,
            "roles": ["data"],
            "proj:epsg": EPSG,
            "proj:wkt2": HWSD_CRS.to_wkt(),
            "proj:bbox": SPATIAL_EXTENT,
            "proj:geometry": get_geometry(),
            "proj:shape": SHAPE,
            "proj:transform": TRANSFORM,
        }),
        "documentation":
        AssetDefinition({
            "types": "application/pdf",
            "roles": ["metadata"],
            "title": "Documentation",
        }),
    }

    return collection


def create_item(
    cog_href: str,
    cog_href_modifier: Optional[ReadHrefModifier] = None,
) -> Item:
    """Create a STAC Item
    Create a STAC Item for one year of the HWSD. The asset_href should include
     the observation year as the first part of the filename.

    Args:
        assets_location (str): The HREF pointing to the location containing all item data assets

    Returns:
        Item: STAC Item object
    """

    geometry = get_geometry()

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

    proj_ext = ProjectionExtension.ext(item, add_if_missing=True)
    proj_ext.epsg = EPSG
    proj_ext.wkt2 = HWSD_CRS.to_wkt()
    proj_ext.bbox = SPATIAL_EXTENT
    proj_ext.geometry = geometry
    proj_ext.shape = SHAPE
    proj_ext.transform = TRANSFORM

    item.add_asset(
        "documentation",
        Asset(media_type="application/pdf",
              roles=["metadata"],
              title="HWSD Documentation",
              href=DOCUMENTATION))

    asset_name = asset_name_from_href(cog_href)
    extra_fields = {
        "units": ASSET_UNITS[asset_name],
    }
    if asset_name in ASSET_NOTES:
        extra_fields["notes"] = ASSET_NOTES[asset_name]
    data_asset = Asset(
        href=cog_href,
        media_type=MediaType.COG,
        roles=["data"],
        title=asset_name,
        description=ASSET_DESCRIPTIONS[asset_name],
        extra_fields={
            "units": ASSET_UNITS[asset_name],
        },
    )
    item.add_asset("data", data_asset)

    # Asset Projection Extension
    data_asset_proj_ext = ProjectionExtension.ext(data_asset,
                                                  add_if_missing=True)
    data_asset_proj_ext.epsg = proj_ext.epsg
    data_asset_proj_ext.wkt2 = proj_ext.wkt2
    data_asset_proj_ext.bbox = proj_ext.bbox
    data_asset_proj_ext.geometry = proj_ext.geometry
    data_asset_proj_ext.shape = proj_ext.shape
    data_asset_proj_ext.transform = proj_ext.transform

    # Include raster information
    rast_ext = RasterExtension.ext(data_asset, add_if_missing=True)
    rast_ext.bands = [
        RasterBand.create(
            nodata=NO_DATA,
            sampling=Sampling.AREA,
            data_type=ASSET_DATA_TYPES[asset_name],
            # spatial_resolution=30,
        )
    ]

    return item
