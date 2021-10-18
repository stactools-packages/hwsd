# flake8: noqa

from typing import Any, Dict

from pyproj import CRS
from pystac import Link, Provider, ProviderRole
from pystac.extensions.raster import DataType

ID = "hwsd"
EPSG = 4326
HWSD_CRS = CRS.from_epsg(EPSG)
SPATIAL_EXTENT = [-180., 90., 180., -90.]
TEMPORAL_EXTENT = ["2000-01-01T00:00:00Z", "2000-12-31T23:59:59Z"]
TITLE = "Harmonized World Soil Database"
DESCRIPTION = "This data set describes select global soil parameters from the Harmonized World Soil Database (HWSD) v1.2, including additional calculated parameters such as area weighted soil organic carbon (kg C per m2), as high resolution NetCDF files. These data were regridded and upscaled from the Harmonized World Soil Database v1.2."
SHAPE = [7200, 3600]
TRANSFORM = [
    0.049999999999999996, 0.0, -180.0, 0.0, -0.049999999999999996, 90.0, 0.0,
    0.0, 1.0
]

HOMEPAGE_REGRIDDED_URL = "https://daac.ornl.gov/SOILS/guides/HWSD.html"
HOMEPAGE_2_URL = "http://webarchive.iiasa.ac.at/Research/LUC/External-World-soil-database/HTML/SoilQualityData.html?sb=11"
HOMEPAGE_1_URL = "https://www.fao.org/soils-portal/data-hub/soil-maps-and-databases/harmonized-world-soil-database-v12"
DOCUMENTATION_URL = "http://daac.ornl.gov/daacdata/global_soil/HWSD/comp/HWSD1.2_documentation.pdf"

LICENSE = "proprietary"
LICENSE_LINK = Link(
    rel="license",
    target="https://earthdata.nasa.gov/earth-observation-data/data-use-policy",
    title="EOSDIS Data Use Policy",
)

PROVIDERS = [
    Provider(name="FAO",
             roles=[
                 ProviderRole.HOST,
                 ProviderRole.LICENSOR,
                 ProviderRole.PROCESSOR,
                 ProviderRole.PRODUCER,
             ],
             url="https://www.fao.org/"),
    Provider(name="IIASA",
             roles=[
                 ProviderRole.LICENSOR,
                 ProviderRole.PRODUCER,
             ],
             url="https://iiasa.ac.at/"),
    Provider(name="ISRIC",
             roles=[
                 ProviderRole.LICENSOR,
                 ProviderRole.PRODUCER,
             ],
             url="https://www.isric.org/"),
    Provider(name="ISS-CAS",
             roles=[
                 ProviderRole.LICENSOR,
                 ProviderRole.PRODUCER,
             ],
             url="http://english.issas.cas.cn/"),
    Provider(name="JRC",
             roles=[
                 ProviderRole.LICENSOR,
                 ProviderRole.PRODUCER,
             ],
             url="https://esdac.jrc.ec.europa.eu/"),
    Provider(name="ORNL",
             roles=[ProviderRole.HOST, ProviderRole.PROCESSOR],
             url="https://www.ornl.gov/"),
    Provider(name="NCAR",
             roles=[ProviderRole.PRODUCER, ProviderRole.PROCESSOR],
             url="https://ncar.ucar.edu/"),
]

KEYWORDS = [
    "HWSD",
    "Soil",
    "Soils",
    "Harmonized World Soil Database",
    "regridded",
]

CITATION = "Wieder, W.R., J. Boehnert, G.B. Bonan, and M. Langseth. 2014. Regridded Harmonized World Soil Database v1.2. Data set. Available on-line [http://daac.ornl.gov] from Oak Ridge National Laboratory Distributed Active Archive Center, Oak Ridge, Tennessee, USA. http://dx.doi.org/10.3334/ORNLDAAC/1247 ."
DOI = "10.3334/ORNLDAAC/1247"

THUMBNAIL_URL = "https://daac.ornl.gov/SOILS/guides/HWSD_Fig1.png"

NO_DATA = -1

ASSET_DATA_TYPES = {
    "AWC_CLASS": DataType.INT16,
    "ISSOIL": DataType.INT16,
    "MU_GLOBAL": DataType.INT32,
    "REF_DEPTH": DataType.INT16,
    "ROOTS": DataType.INT16,
    "T_BULK_DEN": DataType.FLOAT64,
    "S_BULK_DEN": DataType.FLOAT64,
    "T_REF_BULK": DataType.FLOAT64,
    "S_REF_BULK": DataType.FLOAT64,
    "T_CEC_CLAY": DataType.FLOAT64,
    "S_CEC_CLAY": DataType.FLOAT64,
    "T_CLAY": DataType.FLOAT64,
    "S_CLAY": DataType.FLOAT64,
    "T_GRAVEL": DataType.FLOAT64,
    "S_GRAVEL": DataType.FLOAT64,
    "T_SAND": DataType.FLOAT64,
    "S_SAND": DataType.FLOAT64,
    "T_SILT": DataType.FLOAT64,
    "S_SILT": DataType.FLOAT64,
    "T_PH_H2O": DataType.FLOAT64,
    "S_PH_H2O": DataType.FLOAT64,
    "T_C": DataType.FLOAT64,
    "S_C": DataType.FLOAT64,
    "T_OC": DataType.FLOAT64,
    "S_OC": DataType.FLOAT64,
    "AWT_S_SOC": DataType.FLOAT64,
    "AWT_T_SOC": DataType.FLOAT64,
}

ASSET_DESCRIPTIONS = {
    "AWC_CLASS": "Available water storage capacity",
    "ISSOIL": "Soil or non-soil units",
    "MU_GLOBAL": "HWSD global mapping unit identifier",
    "REF_DEPTH": "Reference soil depth",
    "ROOTS": "Depth of obstacles to roots",
    "T_BULK_DEN": "Topsoil bulk density",
    "S_BULK_DEN": "Subsoil bulk density",
    "T_REF_BULK": "topsoil bulk density",
    "S_REF_BULK": "Subsoil reference bulk density",
    "T_CEC_CLAY":
    "Cation exchange capacity of the clay fraction in the topsoil",
    "S_CEC_CLAY":
    "Cation exchange capacity of the clay fraction in the subsoil",
    "T_CLAY": "Topsoil clay fraction",
    "S_CLAY": "Subsoil clay fraction",
    "T_GRAVEL": "Topsoil gravel content",
    "S_GRAVEL": "Subsoil gravel content",
    "T_SAND": "Topsoil sand fraction",
    "S_SAND": "Subsoil sand fraction",
    "T_SILT": "Topsoil silt fraction",
    "S_SILT": "Subsoil silt fraction",
    "T_PH_H2O": "Topsoil pH (in H2O)",
    "S_PH_H2O": "Subsoil pH (in water)",
    "T_C": "Topsoil carbon content",
    "S_C": "Dominant soil type subsoil carbon content",
    "T_OC": "Topsoil organic carbon",
    "S_OC": "Subsoil organic carbon",
    "AWT_S_SOC": "Area weighted subsoil carbon content",
    "AWT_T_SOC": "Area weighted topsoil carbon content",
}

ASSET_UNITS = {
    "AWC_CLASS": "Coded values 1 through 7",
    "ISSOIL": "0 or 1",
    "MU_GLOBAL": "numerical ID",
    "REF_DEPTH": "cm",
    "ROOTS": "Coded values 0 through 6",
    "T_BULK_DEN": "kg dm-3",
    "S_BULK_DEN": "kg dm-3",
    "T_REF_BULK": "kg dm-3",
    "S_REF_BULK": "kg dm-3",
    "T_CEC_CLAY": "cmol per kg",
    "S_CEC_CLAY": "cmol per kg",
    "T_CLAY": "% weight",
    "S_CLAY": "% weight",
    "T_GRAVEL": "% volume",
    "S_GRAVEL": "% volume",
    "T_SAND": "% weight",
    "S_SAND": "% weight",
    "T_SILT": "% weight",
    "S_SILT": "% weight",
    "T_PH_H2O": "-log(H+)",
    "S_PH_H2O": "-log(H+)",
    "T_C": "kg C m-2",
    "S_C": "kg C m-2",
    "T_OC": "% weight",
    "S_OC": "% weight",
    "AWT_S_SOC": "kg C m-2",
    "AWT_T_SOC": "kg C m-2",
}

ASSET_NOTES = {
    "AWC_CLASS":
    "1 = 150 mm water per m of the soil unit, 2 = 125 mm, 3 = 100 mm, 4 = 75 mm, 5 = 50 mm, 6 = 15 mm, 7 = 0 mm.",
    "ISSOIL":
    "ISSOIL indicates whether the soil mapping unit is a soil (1) or non-soil (0)",
    "MU_GLOBAL":
    "MU_GLOBAL provides a link from the grid cell to the other attributes.The HWSD v1.2 attribute lookup table is available from the HWSD project (FAO 2012)",
    "REF_DEPTH":
    "Reference soil depth of all soil units are set at 100 cm, except for Rendzinas and Rankers of FAO-74 and Leptosols of FAO-90, where the reference soil depth is set at 30 cm, and for Lithosols of FAO-74 and Lithic Leptosols of FAO-90, where it is set at 10 cm.",
    "ROOTS":
    "0 = no information, 1 = no obstacles to roots between 0 and 80 cm depth, 2 = obstacles to roots between 60 and 80 cm depth, 3 = obstacles between 40 and 60 cm, 4 = 20 and 40 cm, 5 = 0 and 80 cm, 6 = 0 and 20 cm.",
    "T_REF_BULK":
    "Reference bulk density values are calculated from equations developed by Saxton et al. (1986) that relate to the texture of the soil only. These estimates, although generally reliable, overestimate the bulk density in soils that have a high porosity (Andosols) or that are high in organic matter content (Histosols). The calculation procedures for reference bulk density can be found in Saxton et al (1986)",
    "T_C":
    "Topsoil and subsoil carbon content (T_C and S_C) are based on the carbon content of the dominant soil type in each regridded cell rather than a weighted average.",
    "AWT_S_SOC": "AWT_S_SOC = (sum(SEQ(SHARE * S_OC)) * 7 * S_BULK_DENSITY)",
    "AWT_T_SOC": "AWT_T_SOC = (sum(SEQ(SHARE * T_OC)) * 3 * T_BULK_DENSITY)",
}

ASSET_LABELS = {
    "AWC_CLASS": {
        1: "150 mm per m of the soil unit",
        2: "125 mm per m",
        3: "100 mm per m",
        4: "75 mm per m",
        5: "50 mm per m",
        6: "15 mm per m",
        7: "0 mm per m",
    },
    "ISSOIL": {
        0: "not soil",
        1: "soil",
    },
    "ROOTS": {
        0: "no information",
        1: "no obstacles to roots between 0 and 80 cm depth",
        2: "obstacles to roots between 60 and 80 cm depth",
        3: "obstacle to roots between 40 and 60 cm depth",
        4: "obstacle to roots between 20 and 40 cm depth",
        5: "obstacle to roots between 0 and 80 cm depth",
        6: "obstacle to roots between 0 and 20 cm depth",
    },
}
