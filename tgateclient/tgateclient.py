# -*- coding: utf-8 -*-
import datetime
import hashlib
import hmac
import os
import requests

TIMEOUT = 5

class TGateClient(object):
    def __init__(self, url, username, password):
        self.base_url = url
        self.username = username
        self.password = password

    def _build_headers(self, operation, *args):
        now = datetime.datetime.utcnow()
        timestamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        arguments = ''.join(args)
        datastring = b'{}{}{}'.format(timestamp, arguments, operation)
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
        if response.status_code == 200:
            return response.json()

    def download(self, document_id):
        operation = 'translate/download'
        url = self._build_url(operation)
        headers = self._build_headers(operation, document_id)
        json = {'id': document_id}
        response = requests.post(url, json=json, headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    def remove(self, document_id):
        operation = 'translate/remove_document'
        url = self._build_url(operation)
        headers = self._build_headers(operation, document_id)
        json = {'id': document_id}
        response = requests.post(url, json=json, headers=headers, timeout=TIMEOUT)

        if response.status_code == 200:
            return response.json()
        else:
            return {}

    def get_document_properties(self, document_id):
        operation = 'translate/properties'
        url = self._build_url(operation)
        headers = self._build_headers(operation, document_id)
        json = {'id': document_id}
        response = requests.post(url, json=json, headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    def get_document_status(self, document_id):
        operation = 'translate/status'
        url = self._build_url(operation)
        headers = self._build_headers(operation, document_id)
        json = {'id': document_id}
        response = requests.post(url, json=json, headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    def get_document_id(self, filename):
        operation = 'translate/document_id'
        url = self._build_url(operation)
        headers = self._build_headers(operation, filename)
        json = {'filename': filename}
        response = requests.post(url, json=json, headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            return {}


    def models(self):
        operation = 'translate/models'
        url = self._build_url(operation)
        headers = self._build_headers(operation)
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    def translate_document(self, document_id, model_id, tr_mode):
        operation = 'translate/translate_document'
        url = self._build_url(operation)
        headers = self._build_headers(operation, document_id, model_id)
        json = {
            'document_id': document_id,
            'model_id': model_id,
            'tr_mode': tr_mode,
        }
        response = requests.post(url, json=json, headers=headers, timeout=TIMEOUT)
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
        response = requests.post(url, json=json, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                result['data']['translation'] = self._get_translation_from_result(result['data']['message'])

            return result
        else:
            return {}

    def _get_translation_from_result(self, text):
        """translated text is inside the variable text, after the words 'target text:'
        """
        _, translation = text.split('target text:')
        return translation
