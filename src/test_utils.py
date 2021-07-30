import unittest
import utils


class TestUtils(unittest.TestCase):
    def test_get_root_folder(self):
        actual = utils.get_root_folder()
        self.assertEqual(True, actual.endswith('src'))

    def test_read_conf_file(self):
        actual = utils.read_conf_file()
        self.assertEqual(int(actual['server_config']['server_port']), 7789)
