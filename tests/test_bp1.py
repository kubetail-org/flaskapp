import unittest

from webapp import bp1
from webapp.meta import mail


class TestCase(unittest.TestCase):
    # ==============================
    # Test-level setup/teardown
    # ==============================
    def setUp(self):
        app = bp1.create_app(extra_config={'TESTING': True})
        self.app = app.test_client()

    # ==============================
    # Test methods
    # ==============================
    def test_path1(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('<title>Webapp</title>' in resp.data)

    def test_send_email(self):
        with mail.record_messages() as outbox:
            resp = self.app.get('/send-email')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.data, 'ok')
            self.assertEqual(len(outbox), 1)
            self.assertEqual(outbox[0].subject, 'Subject')


if __name__ == '__main__':
    unittest.main()
