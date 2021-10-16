import os.path
from pathlib import Path
from tempfile import TemporaryDirectory

import pystac
from stactools.testing import CliTestCase

from stactools.hwsd.commands import create_hwsd_command
from stactools.hwsd.constants import DOI, EPSG, ID, LICENSE


class CommandsTest(CliTestCase):
    def create_subcommand_functions(self):
        return [create_hwsd_command]

    def test_create_collection(self):
        with TemporaryDirectory() as tmp_dir:

            result = self.run_command(
                ["hwsd", "create-collection", "-d", tmp_dir])

            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            collection = pystac.read_file(os.path.join(tmp_dir, jsons[0]))
            self.assertEqual(collection.id, ID)
            self.assertEqual(collection.license, LICENSE)
            self.assertEqual(collection.extra_fields["sci:doi"], DOI)
            self.assertEqual(len(collection.extra_fields["item_assets"]), 28)

            collection.validate()

    def test_create_item(self):
        with TemporaryDirectory() as tmp_dir:
            destination = os.path.join(tmp_dir, "item.json")
            result = self.run_command([
                "hwsd",
                "create-item",
                "-s",
                "path/to/assets/",
                "-d",
                destination,
            ])
            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            item = pystac.read_file(destination)
            self.assertEqual(item.id, ID)
            self.assertEqual(item.properties["sci:doi"], DOI)
            self.assertEqual(item.properties["proj:epsg"], EPSG)
            self.assertEqual(len(item.assets), 28)

            item.validate()

    def test_populate_collection(self):
        with TemporaryDirectory() as tmp_dir:
            result = self.run_command([
                "hwsd",
                "populate-collection",
                "-s",
                "path/to/assets/",
                "-d",
                tmp_dir,
            ])
            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [p for p in Path(tmp_dir).rglob('*.json')]
            self.assertEqual(len(jsons), 2)
