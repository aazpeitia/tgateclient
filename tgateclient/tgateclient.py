# -*- coding: utf-8 -*-

"""Main module."""
# -*- coding: utf-8 -*-
import datetime
import hashlib
import hmac
import httplib
import logging
import os
import requests

class TGateClient(object):
    def __init__(self, url, username, password):
        self.base_url = url
        self.username = username
        self.password = password

    def _build_headers(self, operation, *args):
        now = datetime.datetime.utcnow()
        timestamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        arguments = ''.join(args)
        datastring = '{}{}{}'.format(timestamp, arguments, operation)
        data = hmac.new(self.password, datastring, hashlib.sha512).hexdigest()
        headers = {
            'client': self.username,
            'timestamp': timestamp,
            'data': data,
        }
        return headers

    def _build_url(self, operation):
        return self.base_url + operation

    def hello(self):
        operation = 'test/hello'
        url = self._build_url(operation)
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            return None

    def upload(self, filename):
        operation = 'translate/upload'
        url = self._build_url(operation)
        headers = self._build_headers(operation, os.path.basename(filename))
        files = {'file': (os.path.basename(filename), open(filename, 'rb'), 'application/octet-stream')}
        response = requests.post(url, files=files, headers=headers)
        print(response.status_code)
        print(response.content)

    def models(self):
        operation = 'translate/models'
        url = self._build_url(operation)
        headers = self._build_headers(operation)
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    def translate_string(self, text, model_id, tr_mode, mime_type):
        operation = 'translate/translate_string'
        url = self._build_url(operation)
        headers = self._build_headers(operation, text, model_id, mime_type)
        json = {
            'text': text,
            'model_id': model_id,
            'tr_mode': tr_mode,
            'mime': mime_type
        }
        response = requests.post(url, json=json, headers=headers, timeout=2)
        print(response.status_code)
        print(response.content)


