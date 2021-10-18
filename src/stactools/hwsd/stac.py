import logging
import os
from typing import Any, Dict, List, Optional

import fsspec
from pystac import (
    CatalogType,
    Collection,
    Extent,
    MediaType,
    SpatialExtent,
    TemporalExtent,
)
from pystac.asset import Asset
from pystac.extensions.file import FileExtension
from pystac.extensions.item_assets import AssetDefinition, ItemAssetsExtension
from pystac.extensions.label import (
    LabelClasses,
    LabelExtension,
    LabelTask,
    LabelType,
)
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
    ASSET_LABELS,
    ASSET_NOTES,
    ASSET_UNITS,
    CITATION,
    DESCRIPTION,
    DOCUMENTATION_URL,
    DOI,
    EPSG,
    HOMEPAGE_1_URL,
    HOMEPAGE_2_URL,
    HOMEPAGE_REGRIDDED_URL,
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
    THUMBNAIL_URL,
    TITLE,
    TRANSFORM,
)

logger = logging.getLogger(__name__)


def asset_name_from_href(href: str) -> str:
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
    collection.add_link(
        Link(RelType.VIA, target=HOMEPAGE_1_URL, title="Homepage"))
    collection.add_link(
        Link(RelType.VIA, target=HOMEPAGE_2_URL, title="Homepage, Alternate"))
    collection.add_link(
        Link(RelType.VIA,
             target=HOMEPAGE_REGRIDDED_URL,
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
            roles=["documentation", "metadata"],
            title="Documentation",
            href=DOCUMENTATION_URL,
        ))

    collection.add_asset(
        "thumbnail",
        Asset(
            media_type=MediaType.PNG,
            roles=["thumbnail"],
            title="Thumbnail",
            href=THUMBNAIL_URL,
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
            "roles": ["documentation", "metadata"],
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

    if cog_href_modifier is not None:
        cog_access_href = cog_href_modifier(cog_href)
    else:
        cog_access_href = cog_href

    asset_name = asset_name_from_href(cog_href)
    geometry = get_geometry()
    properties = {
        "title": asset_name,
        "description": ASSET_DESCRIPTIONS[asset_name],
        "start_datetime": TEMPORAL_EXTENT[0],
        "end_datetime": TEMPORAL_EXTENT[1],
    }

    item = Item(
        id=asset_name,
        geometry=geometry,
        bbox=SPATIAL_EXTENT,
        datetime=str_to_datetime(TEMPORAL_EXTENT[0]),
        properties=properties,
    )

    item.add_link(Link(RelType.VIA, target=HOMEPAGE_1_URL, title="Homepage"))
    item.add_link(
        Link(RelType.VIA, target=HOMEPAGE_2_URL, title="Homepage, Alternate"))
    item.add_link(
        Link(RelType.VIA,
             target=HOMEPAGE_REGRIDDED_URL,
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
              roles=["documentation", "metadata"],
              title="HWSD Documentation",
              href=DOCUMENTATION_URL))

    extra_fields = {
        "units": ASSET_UNITS[asset_name],
    }
    if asset_name in ASSET_NOTES:
        extra_fields["notes"] = ASSET_NOTES[asset_name]
    roles = ["data"]
    if asset_name in ASSET_LABELS:
        roles.extend(["labels", "labels-raster"])
    data_asset = Asset(
        href=cog_href,
        media_type=MediaType.COG,
        roles=roles,
        title=asset_name,
        description=ASSET_DESCRIPTIONS[asset_name],
        extra_fields=extra_fields,
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

    # Label Extension
    if asset_name in ASSET_LABELS:
        item_label = LabelExtension.ext(item, add_if_missing=True)
        item_label.label_type = LabelType.RASTER
        item_label.label_tasks = [LabelTask.CLASSIFICATION]
        item_label.label_properties = None
        item_label.label_description = ASSET_DESCRIPTIONS[asset_name]
        item_label.label_classes = [
            # TODO: The STAC Label extension JSON Schema is incorrect.
            # https://github.com/stac-extensions/label/pull/8
            # https://github.com/stac-utils/pystac/issues/611
            # When it is fixed, this should be None, not the empty string.
            LabelClasses.create(list(ASSET_LABELS[asset_name].values()), "")
        ]

    # File Extension
    data_asset_file_ext = FileExtension.ext(data_asset, add_if_missing=True)
    if asset_name in ASSET_LABELS:
        # The following odd type annotation is needed
        mapping: List[Any] = [{
            "values": [value],
            "summary": summary,
        } for value, summary in ASSET_LABELS[asset_name].items()]
        data_asset_file_ext.values = mapping
    with fsspec.open(cog_access_href) as file:
        size = file.size
        if size is not None:
            data_asset_file_ext.size = size

    # Raster Extension
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
