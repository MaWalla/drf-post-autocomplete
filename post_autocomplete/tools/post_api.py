import json
import requests
from urllib.parse import urljoin
from zoneinfo import ZoneInfo

from django.conf import settings
from django.utils import timezone

from requests.auth import HTTPBasicAuth
from post_autocomplete.models import PostAccessToken

from .mock_api import PostMockRequest


__all__ = ['search_buildings']


mock_request = PostMockRequest()


def get_token():
    now = timezone.now() + timezone.timedelta(minutes=1)  # add a grace period to the token can't expire during the call
    latest_token = PostAccessToken.objects.filter(expires__gt=now).last()

    url = urljoin(settings.POST_AUTOCOMPLETE_URL, 'token')

    if not latest_token:
        if settings.MOCK_API:
            token_response = mock_request.token()
        else:
            token_response = requests.get(
                url,
                auth=HTTPBasicAuth(settings.POST_DATAFACTORY_USER, settings.POST_DATAFACTORY_PASSWORD),
            )

        content = json.loads(token_response.content or 'null')

        if content:
            access_token = PostAccessToken(
                token=content.get('access_token'),
                expires=timezone.datetime.fromtimestamp(
                    content.get('expires_in_epoch_seconds'),
                    tz=ZoneInfo('Europe/Berlin'),
                ),
            )

            PostAccessToken.objects.all().delete()
            access_token.save()
            return access_token

        return None

    return latest_token


def autocomplete_api_call(endpoint, params, recursion=False):
    url = urljoin(settings.POST_AUTOCOMPLETE_URL, endpoint)

    headers = {}
    token_object = get_token()
    if token_object:
        headers = {'Authorization': f'Bearer {token_object.token}'}

    if settings.MOCK_API:
        response = mock_request.handle_request(url, 'GET', headers, params)
    else:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False,
        )

    if response.status_code == 200:
        return json.loads(response.content)

    if response.status_code == 401 and not recursion:
        return autocomplete_api_call(endpoint, params, True)


def search_buildings(country='de', combined=None, **kwargs):
    """
    :param country: country to use in the endpoint, defaults to 'de'
    :param combined: combined query param. Overrides the kwargs when used
    :param kwargs: can be the following: postal_code, city, district, street, house_number, distribution_code
    :return: results as a list of dicts
    """
    if combined:
        params = {'combined': combined}
    else:
        params = kwargs

    content = autocomplete_api_call(f'search/{country}/buildings', params)

    if content:
        return content.get('buildings', [])

    return []
