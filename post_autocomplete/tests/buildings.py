from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase

from post_autocomplete.tools.mock_api import MOCK_TOKEN


__all__ = ['BuildingsTests']


@override_settings(MOCK_API=True)
class BuildingsTests(APITestCase):

    def setUp(self):
        self.authorization_header = {'HTTP_Authorization': MOCK_TOKEN}

    def test_retrieve_buildings(self):
        expected_data = [{
            'uuid': '12345678-abcd-0987-fedc-12345678abcd',
            'postalCode': '12345',
            'city': 'Musterstadt',
            'district': 'Mustermitte',
            'street': 'Musterstr.',
            'houseNumber': '1',
            'distributionCode': '12345000000',
        }]

        response = self.client.get(
            reverse('api-search-buildings'),
            headers=self.authorization_header,
            data={'postal_code': '12345'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)
