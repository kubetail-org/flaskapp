import unittest

from webapp import bp2


class TestCase(unittest.TestCase):
    # ==============================
    # Test-level setup/teardown
    # ==============================
    def setUp(self):
        app = bp2.create_app(extra_config={'TESTING': True})
        self.app = app.test_client()

    # ==============================
    # Test methods
    # ==============================
    def test_path1(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('<title>Webapp</title>' in resp.data)


if __name__ == '__main__':
    unittest.main()
