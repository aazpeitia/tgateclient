#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `tgateclient` package."""
from tgateclient import tgateclient

import os
import six
import pytest


@pytest.fixture
def client():
    server_name = os.environ.get('TGATE_SERVER_URL')
    username = os.environ.get('TGATE_USERNAME')
    password = os.environ.get('TGATE_PASSWORD')
    return tgateclient.TGateClient(server_name, username, password)


def test_hello(client):
    hello_answer = client.hello()
    assert six.b("Translation Service says: hello") in hello_answer

@pytest.mark.xfail
def test_upload_html(client):
    testhtml = os.path.dirname(os.path.abspath(__file__)) + '/files/' + 'test.html'
    response = client.upload(testhtml)
    assert isinstance(response, dict)
    assert 'status' in response
    assert response.get('status') == 'success'
    assert 'data' in response
    assert isinstance(response.get('data', {}), dict)
    assert 'id' in response.get('data', {})

def test_upload_docx(client):
    testdocx = os.path.dirname(os.path.abspath(__file__)) + '/files/' + 'test1.docx'
    response = client.upload(testdocx)
    assert isinstance(response, dict)
    assert 'status' in response
    assert response.get('status') == 'success'
    assert 'data' in response
    assert isinstance(response.get('data', {}), dict)
    assert 'id' in response.get('data', {})

def test_download_unkown_document(client):
    response = client.download('this-is-an-unkown-document-id')
    assert isinstance(response, dict)
    assert 'status' in response
    assert response.get('status') == 'error'

def test_download_uploaded_document(client):
    testdocx = os.path.dirname(os.path.abspath(__file__)) + '/files/' + 'test2.docx'
    response = client.upload(testdocx)
    result = response.get('data', {})
    document_id = result.get('id', None)
    response = client.download(document_id)
    assert isinstance(response, dict)
    assert 'status' in response
    assert response.get('status', '') == 'success'
    assert 'data' in response
    assert 'id' in response.get('data', {})
    assert response.get('data', {}).get('id').startswith('http')

def test_remove_unkown_document(client):
    response = client.remove('this-is-an-unkown-document-id')
    assert isinstance(response, dict)
    assert 'status' in response
    assert response.get('status') == 'error'

def test_remove_uploaded_document(client):
    testdocx = os.path.dirname(os.path.abspath(__file__)) + '/files/' + 'test3.docx'
    response = client.upload(testdocx)
    result = response.get('data', {})
    document_id = result.get('id', None)
    response = client.remove(document_id)
    assert isinstance(response, dict)
    assert 'status' in response
    assert response.get('status', '') == 'success'
    assert 'data' in response
    assert 'id' in response.get('data', {})
    assert response.get('data', {}).get('id') == document_id

def test_get_document_properties_unkown_document(client):
    response = client.get_document_properties('this-is-an-unkown-document-id')
    assert isinstance(response, dict)
    assert 'status' in response
    assert response.get('status') == 'error'

def test_get_document_properties_uploaded_document(client):
    testdocx = os.path.dirname(os.path.abspath(__file__)) + '/files/' + 'test4.docx'
    response = client.upload(testdocx)
    result = response.get('data', {})
    document_id = result.get('id', None)
    response = client.get_document_properties(document_id)
    assert isinstance(response, dict)
    assert 'status' in response
    assert response.get('status', '') == 'success'
    assert 'data' in response
    assert 'id' in response.get('data', {})
    assert response.get('data', {}).get('id')

def test_get_document_status_unknown_document(client):
    response = client.get_document_status('this-is-an-unkown-document-id')
    assert isinstance(response, dict)
    assert 'status' in response
    assert response.get('status') == 'error'

def test_get_document_status_uploaded_document_ready_to_translate(client):
    testdocx = os.path.dirname(os.path.abspath(__file__)) + '/files/' + 'test5.docx'
    response = client.upload(testdocx)
    result = response.get('data', {})
    document_id = result.get('id', None)
    response = client.get_document_status(document_id)
    assert isinstance(response, dict)
    assert 'status' in response
    assert response.get('status', '') == 'success'
    assert 'data' in response
    assert 'id' in response.get('data', {})
    assert response.get('data', {}).get('id') == 'READY'

@pytest.mark.xfail
def test_get_document_status_uploaded_document_translating(client):
    testdocx = os.path.dirname(os.path.abspath(__file__)) + '/files/' + 'test6.docx'
    response = client.upload(testdocx)
    result = response.get('data', {})
    document_id = result.get('id', None)
    model_id = 'en2es'
    tr_mode = 'MachineTranslation'
    response = client.translate_document(document_id, model_id, tr_mode)
    assert 'status' in response
    assert response.get('status', '') == 'success'
    response = client.get_document_status(document_id)
    assert isinstance(response, dict)
    assert 'status' in response
    assert response.get('status', '') == 'success'
    assert 'data' in response
    assert 'id' in response.get('data', {})
    assert response.get('data', {}).get('id') == 'TRANSLATING'

def test_get_document_id(client):
    response = client.get_document_id('test.docx')
    assert isinstance(response, dict)
    assert 'status' in response
    assert response.get('status', '') == 'success'
    assert 'data' in response
    assert 'id' in response.get('data', {})
    assert response.get('data', {}).get('id', '')

def test_get_models(client):
    models_answer = client.models()
    assert isinstance(models_answer, dict)
    assert 'status' in models_answer
    assert models_answer.get('status') == 'success'
    assert 'data' in models_answer
    assert 'models' in models_answer
    assert isinstance(models_answer.get('models', []), list)

@pytest.mark.xfail
def test_translate_document(client):
    testdocx = os.path.dirname(os.path.abspath(__file__)) + '/files/' + 'test7.docx'
    response = client.upload(testdocx)
    result = response.get('data', {})
    document_id = result.get('id', None)
    model_id = 'generic_es2en'
    tr_mode = 'MachineTranslation'
    response = client.translate_document(document_id, model_id, tr_mode)
    assert isinstance(response, dict)
    assert 'status' in response
    assert response.get('status', '') == 'success'
    assert 'data' in response
    assert 'id' in response.get('data', {})
    assert response.get('data', {}).get('id') == document_id


def test_translate_string(client):
    testhtml = os.path.dirname(os.path.abspath(__file__)) + '/files/' + 'test.txt'
    with open(testhtml, 'r') as fp:
        model_id = 'generic_es2en'
        tr_mode = 'MachineTranslation'
        mime_type = 'text/plain'
        response = client.translate_string(fp.read(), model_id, tr_mode, mime_type)
        assert isinstance(response, dict)
        assert 'status' in response
        assert response.get('status', '') == 'success'
        assert 'data' in response
        assert 'id' in response.get('data', {})
        assert response.get('data', {}).get('translation', '')
