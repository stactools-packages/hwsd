import unittest

from stactools.hwsd import stac
from stactools.hwsd.constants import DOI, EPSG, ID, LICENSE


class StacTest(unittest.TestCase):
    def test_create_collection(self):
        collection = stac.create_collection()
        collection.set_self_href("")

        self.assertEqual(collection.id, ID)
        self.assertEqual(collection.license, LICENSE)
        self.assertEqual(collection.extra_fields["sci:doi"], DOI)
        self.assertEqual(len(collection.extra_fields["item_assets"]), 28)

        collection.validate()

    def test_create_item(self):
        item = stac.create_item("path/to/files/1900.csv.gz")

        self.assertEqual(item.id, ID)
        self.assertEqual(item.properties["sci:doi"], DOI)
        self.assertEqual(item.properties["proj:epsg"], EPSG)
        self.assertEqual(len(item.assets), 28)

        # Validate
        item.validate()
