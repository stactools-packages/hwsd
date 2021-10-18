import os
import unittest

from stactools.hwsd import stac
from stactools.hwsd.constants import DOI, EPSG, ID, LICENSE
from tests import test_data


class StacTest(unittest.TestCase):
    def test_create_collection(self):
        collection = stac.create_collection()
        collection.set_self_href("")

        self.assertEqual(collection.id, ID)
        self.assertEqual(collection.license, LICENSE)
        self.assertEqual(collection.extra_fields["sci:doi"], DOI)
        self.assertEqual(len(collection.extra_fields["item_assets"]), 2)

        collection.validate()

    def test_create_classification_item(self):
        test_path = test_data.get_path("data-files")
        item = stac.create_item(os.path.join(test_path, "AWC_CLASS.tif"))

        self.assertEqual(item.id, "AWC_CLASS")
        self.assertEqual(item.properties["sci:doi"], DOI)
        self.assertEqual(item.properties["proj:epsg"], EPSG)
        self.assertEqual(len(item.assets), 2)
        # TODO: Check Label and File extensions

        # Validate
        item.validate()

    def test_create_item(self):
        test_path = test_data.get_path("data-files")
        in_file = os.path.join(test_path, "T_GRAVEL.tif")
        print(in_file)
        item = stac.create_item(in_file)

        self.assertEqual(item.id, "T_GRAVEL")
        self.assertEqual(item.properties["sci:doi"], DOI)
        self.assertEqual(item.properties["proj:epsg"], EPSG)
        self.assertEqual(len(item.assets), 2)

        # Validate
        item.validate()
