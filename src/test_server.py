import unittest
import requests


class TestAPI(unittest.TestCase):
    def test_search_api_package_found(self):
        res = requests.get('http://localhost:7789/search?q=A3')
        resp_body = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 3)
        self.assertEqual(resp_body['message'], "Package details found.")
        self.assertEqual(resp_body['data'][0]['Author'], "Scott Fortmann-Roe")

    def test_search_api_package_not_found(self):
        res = requests.get('http://localhost:7789/search?q=A4')
        resp_body = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 3)
        self.assertEqual(resp_body['message'], "No package details found.")
        self.assertEqual(len(resp_body['data']), 0)
