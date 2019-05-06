from django.test import SimpleTestCase


class AboutPageTests(SimpleTestCase):

    def test_about_page_status_code(self):
        response = self.client.get('/ppra_test')
        self.assertEquals(response.status_code, 200)