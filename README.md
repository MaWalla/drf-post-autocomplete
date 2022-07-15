# DATAFACTORY Autocomplete 2.0 API implementation

## Some insights

This Django app was made, because I had troubles working with the Autocomplete 2.0 API.

While they offer nice documentation for the available endpoints, I could find no information on how authorization works and had to find that out myself.

Independent of Python / Django, this is how I made it work:

First, you'll need a token, which is used for all other endpoints. It can be acquired by making a GET request on the `/token` endpoint.

Here you have to authorize with HTTP Basic Auth. Check how your library does it, for Python requests it works like this:

```
requests.get(token_url, auth=HTTPBasicAuth(username, password))
```

Out of this, you'll get an `access_token` and `expires_in_epoch_seconds`. As of writing this, the token expires rather quickly, so be prepared to refresh it on a regular basis.

For all further requests, you need to use the access token and set it as Bearer token in the Authorization header. Again for Python requests it works like this:

```
requests.get(
    enpoint_url,
    headers={'Authorization': f'Bearer {access_token}'},
    params=get_params,
)
```

With this, requests to the API should succeed!

## Usage of this app

At the time, there is no pip package. You can still install it with pip though, by running: 

`pip install git+https://github.com/MaWalla/drf-post-autocomplete`

or putting `git+https://github.com/MaWalla/drf-post-autocomplete` in your requirements.txt

With this done, you'll have to add `post_autocomplete` to your `INSTALLED_APPS`.

Now you can apply the migration by running `python manage.py migrate`. It is required for caching the token between requests.

To use the provided endpoints, you'll have to add the following to `urls.py`:

`path('api/', include('post_autocomplete.urls')),`

Adjust the route as needed. In this example, the buildings endpoint is available under `/api/post/search-buildings`

Finally, there are 3 entries that need to be added to your settings.py

| setting                   | description                                                 |
|---------------------------|-------------------------------------------------------------|
| POST_AUTOCOMPLETE_URL     | You'll get that one from their provided documentation.      |
| POST_DATAFACTORY_USER     | The username, also used for logging into the web interface. |
| POST_DATAFACTORY_PASSWORD | The password, also used for logging into the web interface. |

I recommend using `os.getenv()` or something similar to set username and password

## Routes

  - `post/search-buildings`
    - request params:
      - `postal_code`, string, maximum length: 10, optional
      - `city`, string, maximum length: 128, optional
      - `district`, string, maximum length: 128, optional
      - `street`, string, maximum length: 128, optional
      - `house_number`, string, maximum length: 128, optional
      - `distribution_code`, string, maximum length: 128, optional
      - `combined`, string, maximum length: 128, optional
    - response:
      - `uuid`, string
      - `postalCode`, string
      - `city`, string
      - `district`, string
      - `street`, string
      - `houseNumber`, string
      - `distributionCode`, string

## Contributing

So far, I've only implemented the authorization workflow and search buildings endpoint for Germany, because it fits my needs.

There are many more endpoints available though, which I may implement in the future. 

Of course, pull requests that help in completing the implementation are much appreciated too!

