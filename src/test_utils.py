import unittest
import utils


class TestUtils(unittest.TestCase):
    def test_get_root_folder(self):
        actual = utils.get_root_folder()
        self.assertEqual(True, actual.endswith('src'))

    def test_read_conf_file(self):
        actual = utils.read_conf_file()
        self.assertEqual(int(actual['server_config']['server_port']), 7789)

    def test_read_package_description_success(self):
        package_path = utils.get_root_folder()+"/../packages"
        resp = utils.read_package_description(package_path, "A3")
        pack_data = resp['data']
        self.assertEqual(resp["code"], 200)
        self.assertEqual(
            resp["message"], "Package data retrieved successfully")
        self.assertEqual(pack_data['Package'], "A3")

    def test_read_package_description_should_get_file_not_found(self):
        package_path = utils.get_root_folder()+"/../packages"
        resp = utils.read_package_description(package_path, "A4")
        self.assertEqual(resp["code"], 40003)
        self.assertEqual(resp["message"], "File not found")

    def test_download_extract_should_success(self):
        resp = utils.download_and_extract_tarfile("A3", "1.0.0")
        self.assertEqual(resp["code"], 200)
        self.assertEqual(
            resp["message"], "Package downloaded and uncomressed successfully")

    def test_download_extract_should_fail(self):
        resp = utils.download_and_extract_tarfile("A3A3", "1.0.0")
        self.assertEqual(resp["code"], 40002)
        self.assertEqual(
            resp["message"], "HTTP Error 404: Not Found")

    def test_get_package_list_should_pass(self):
        resp = utils.get_package_list(
            "http://cran.r-project.org/src/contrib/PACKAGES")
        self.assertEqual(resp['code'], 200)
        self.assertGreaterEqual(len(resp['data']), 17949)

    def test_get_package_list_should_fail(self):
        resp = utils.get_package_list(
            "http://cran.r-project.org/src/contrib/PACKAGES11")
        self.assertEqual(resp['code'], 40004)

    def test_find_package_in_db_success(self):
        resp = utils.find_package('A3')
        self.assertEqual(resp['message'], "Package details found.")

    def test_find_package_in_db_not_found(self):
        resp = utils.find_package('A4')
        self.assertEqual(resp['message'], "No package details found.")
