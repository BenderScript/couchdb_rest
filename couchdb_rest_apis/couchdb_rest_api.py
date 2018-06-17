#! /usr/bin/env python3

"""
CouchDB REST APIs
"""

from http import HTTPStatus
from magen_rest_apis.rest_client_apis import RestClientApis


__author__ = "rapenno@gmail.com"
__copyright__ = "Copyright(c) 2018, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__license__ = "BSD"


def create_db(url, db_name, overwrite=False):
    """
    Creates a DB in couchDB
    :param overwrite: whether to overwrite db if it exists
    :param url: couchDB base URL in format http://host:port/
    :param db_name:  name of db to be created
    :return: boolean
    """
    if overwrite:
        delete_db(url, db_name)
    put_resp = RestClientApis.http_put_and_check_success(url + db_name, "{}")
    if put_resp.http_status == HTTPStatus.CREATED:
        return 0
    else:
        return -1


def delete_db(url, db_name):
    """
    Deletes a DB from couchDB
    :param url: couchDB base URL in format http://host:port/
    :param db_name: name of db to be deleted
    :return: boolean
    """
    del_resp = RestClientApis.http_delete_and_check_success(url + db_name)
    if del_resp.success:
        return 0
    else:
        return -1


def create_named_document(url, db_name, doc_name, document):
    """

    :param url: couchDB base URL in format http://host:port/
    :param db_name:name of db
    :param doc_name: document name
    :param document: document as a json string
    :return: boolean
    """
    doc_url = url + db_name + "/" + doc_name
    put_resp = RestClientApis.http_put_and_check_success(doc_url, document)
    if put_resp.http_status == HTTPStatus.CREATED:
        return 0
    else:
        return -1


def get_named_document(url, db_name, doc_name):
    """
    Retrieve the named document
    :param url: couchDB base URL in format http://host:port/
    :param db_name:name of db
    :param doc_name: document name
    :return: document or None
    """
    doc_url = url + db_name + "/" + doc_name
    get_resp = RestClientApis.http_get_and_check_success(doc_url)
    if get_resp.http_status == HTTPStatus.OK:
        return get_resp.json_body
    else:
        return None

