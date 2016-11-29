import hashlib
import hmac
import json
from datetime import datetime, timedelta

import requests

ASSEMBLY_API_URL = 'http://api2.transloadit.com/assemblies'


class Client(object):
    def __init__(self, key, secret, api=None):
        self.key = key
        self.secret = secret
        if api:
            self.api = api
        else:
            self.api = ASSEMBLY_API_URL

    def _sign_request(self, params):
        return hmac.new(self.secret, json.dumps(params),
            hashlib.sha1).hexdigest()

    def get_auth(self):
        return {
            'key': self.key,
            'expires': (datetime.now() +
                timedelta(days=1)).strftime('%Y/%m/%d %H:%M:%S')
        }

    def post(self, path="", files=None, **params):
        url = "{}{}".format(ASSEMBLY_API_URL, path)

        if 'auth' not in params:
            params['auth'] = self.get_auth()

        response = requests.post(url, data={
            'params': json.dumps(params),
            'signature': self._sign_request(params)
        }, files=files)

        return response

    def get(self, files=None, **params):
        if 'auth' not in params:
            params['auth'] = self.get_auth()

        response = requests.get(ASSEMBLY_API_URL, params={'params': json.dumps(params),
            'signature': self._sign_request(params)})

        return response.json()

    def reply(self, video_id):
        path = "/{}/reply".format(video_id)
        response = self.post(path)
        return response.json()
