import json
from urllib.parse import urljoin
from zoneinfo import ZoneInfo

from django.conf import settings

import requests
from django.utils import timezone
from requests.auth import HTTPBasicAuth


__all__ = ['search_buildings']

from post_autocomplete.models import PostAccessToken


def get_token():
    now = timezone.now() + timezone.timedelta(minutes=1)  # add a grace period to the token can't expire during the call
    latest_token = PostAccessToken.objects.filter(expires__gt=now).last()

    if not latest_token:
        token_response = requests.get(
            urljoin(settings.POST_AUTOCOMPLETE_URL, 'token'),
            auth=HTTPBasicAuth(settings.POST_DATAFACTORY_USER, settings.POST_DATAFACTORY_PASSWORD)
        )

        content = json.loads(token_response.content)

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


def autocomplete_api_call(endpoint, params):
    token_object = get_token()

    response = requests.get(
        urljoin(settings.POST_AUTOCOMPLETE_URL, endpoint),
        headers={'Authorization': f'Bearer {token_object.token}'},
        params=params,
        allow_redirects=False,
    )

    if response.status_code == 200:
        return json.loads(response.content)


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
