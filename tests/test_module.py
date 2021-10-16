import unittest

import stactools.hwsd


class TestModule(unittest.TestCase):
    def test_version(self):
        self.assertIsNotNone(stactools.hwsd.__version__)
