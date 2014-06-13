import unittest

from webapp import bp1


class TestCase(unittest.TestCase):
    # ==============================
    # Test-level setup/teardown
    # ==============================
    def setUp(self):
        app = bp1.create_app()
        app.config['TESTING'] = True
        self.app = app.test_client()

    # ==============================
    # Test methods
    # ==============================
    def test_path1(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('<title>Webapp</title>' in resp.data)


if __name__ == '__main__':
    unittest.main()
