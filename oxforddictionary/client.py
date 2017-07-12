import requests
from urllib.parse import urljoin

from oxforddictionary.models import word_list, retrieve_entry


class client(object):
    def __init__(self, app_id, app_key, source_lang="en"):
        # String, id of application
        self.app_id = app_id
        # String, key for application
        self.app_key = app_key
        # String, IANA language code for default language
        self.source_lang = source_lang
        # OED API base URL
        self.base_url = "https://od-api.oxforddictionaries.com:443/api/v1/"

    # Returns a string that is the url to use for the request
    def _url(self, api_path, word_id=None, source_lang=None, filters=None):
        if source_lang is None:
            source_lang = self.source_lang
        api_path = api_path + '/' + source_lang
        if word_id:
            api_path = api_path + '/' + word_id
        if filters:
            api_path = api_path + '/' + self._filters(filters)
        return urljoin(self.base_url, api_path)

    def _request(self, url, add_parameters={}, add_headers={}):
        parameters = {}
        headers = {}
        headers['app_id'] = self.app_id
        headers['app_key'] = self.app_key

        # Concat dicts
        for k, v in add_headers.items():
            headers[k] = v
        for k, v in add_parameters.items():
            parameters[k] = v

        r = requests.get(url, params=parameters, headers=headers)
        return r

    # TODO: implement regions and prefix
    def search(self, query, source_lang=None, prefix=False, regions=None,
               limit=1, offset=0):
        url = self._url('search', source_lang=source_lang)
        parameters = {}
        parameters['q'] = query.lower()
        if prefix:
            parameters['prefix'] = True
        else:
            parameters['prefix'] = False
        # parameters['regions']
        parameters['limit'] = limit
        parameters['offset'] = offset

        r = self._request(url, add_parameters=parameters)
        return word_list(r.json())

    def _filters(self, filters):
        filter_array = [k + ("" if v is None else "={}".format(v)) for k, v in
                        filters.items()]
        if len(filter_array) == 0:
            return None
        return ';'.join(filter_array)

    # Filter needs to be a dictionary, implement filter function to construct
    # the blob
    def entries(self, word_id, source_lang=None, regions=None, filters=None,
                category=None):
        url = self._url('entries', word_id=word_id, filters=filters,
                        source_lang=source_lang)
        # entries has no GET params
        r = self._request(url)
        return retrieve_entry(r.json())
