from . import WebsiteTestCase


class ContentTests(WebsiteTestCase):
    def test_pages(self):
        urls = [
            '/'
            ]

        # test that content pages return 200 status code
        for url in urls:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200, url)
