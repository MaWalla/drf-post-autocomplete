import json
from urllib.parse import urljoin

from django.conf import settings


__all__ = ['MockResponse', 'PostMockRequest', 'MOCK_TOKEN']


MOCK_TOKEN = '1234567890abcdef'


class MockResponse:

    def __init__(self, content, status_code=200):
        self.content = json.dumps(content)
        self.status_code = status_code


class PostMockRequest:

    def handle_request(self, url, method, headers, params=dict()):
        url_map = {
            'search/de/buildings': self.buildings,
        }

        url_map = {urljoin(settings.POST_AUTOCOMPLETE_URL, key): value for key, value in url_map.items()}

        # TODO validate HTTP BasicAuth

        if headers.get('Authorization') == f'Bearer {MOCK_TOKEN}' and method.upper() == 'GET':
            endpoint_method = url_map.get(url)
            return endpoint_method(params)

        return MockResponse({}, 401)

    def token(self, *args, **kwargs):
        return MockResponse({
            'access_token': MOCK_TOKEN,
            'expires_in_epoch_seconds': 1645564920,  # 22.02.2022 22:22
        })

    def buildings(self, params=dict()):
        if params.get('postal_code') == '12345':
            return MockResponse({
                'buildings': [{
                    'uuid': '12345678-abcd-0987-fedc-12345678abcd',
                    'postalCode': '12345',
                    'city': 'Musterstadt',
                    'district': 'Mustermitte',
                    'street': 'Musterstr.',
                    'houseNumber': '1',
                    'distributionCode': '12345000000',
                }],
            })
        return MockResponse({}, 400)
