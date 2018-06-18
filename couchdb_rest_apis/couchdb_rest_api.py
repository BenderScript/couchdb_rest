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
__license__ = "Apache"

# TODO Replace print by logs


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


def create_named_document(url, db_name, doc_name, document, overwrite=False):
    """

    :param overwrite: Should we create a new revision if doc exists?
    :param url: couchDB base URL in format http://host:port/
    :param db_name:name of db
    :param doc_name: document name
    :param document: document as a json string
    :return: Json body as dict or None
    """
    doc_url = url + db_name + "/" + doc_name
    if overwrite:
        get_resp = RestClientApis.http_get_and_check_success(doc_url)
        if get_resp.http_status == HTTPStatus.OK:
            rev = get_resp.json_body["_rev"]
            rev_json = '"_rev":"{}",'.format(rev)
            document = document.replace('{', '{' + rev_json, 1)
        elif get_resp.http_status == HTTPStatus.NOT_FOUND:
            print("Overwrite requested but document does not exist \n")
        elif get_resp.http_status == HTTPStatus.UNAUTHORIZED:
            print("Overwrite requested but not enough permissions \n")
            return None
        else:
            print("Unknown error, HTTP Code {}".format(get_resp.http_status))
            return None
    put_resp = RestClientApis.http_put_and_check_success(doc_url, document)
    if put_resp.http_status == HTTPStatus.CREATED:
        return put_resp.json_body
    else:
        return None


def get_named_document(url, db_name, doc_name):
    """
    Retrieve the named document
    :param url: couchDB base URL in format http://host:port/
    :param db_name:name of db
    :param doc_name: document name
    :return: document as json dict or None
    """
    doc_url = url + db_name + "/" + doc_name
    get_resp = RestClientApis.http_get_and_check_success(doc_url)
    if get_resp.http_status == HTTPStatus.OK:
        return get_resp.json_body
    else:
        return None


def delete_named_document(url, db_name, doc_name):
    """
    Delete the named document
    :param url: couchDB base URL in format http://host:port/
    :param db_name:name of db
    :param doc_name: document name
    :return: delete result or None
    """
    doc_url = url + db_name + "/" + doc_name
    get_resp = RestClientApis.http_get_and_check_success(doc_url)
    if get_resp.http_status == HTTPStatus.OK:
        rev = get_resp.json_body["_rev"]
        doc_url = doc_url + "?rev=" + rev
    elif get_resp.http_status == HTTPStatus.UNAUTHORIZED:
        print("Delete requested but not enough permissions \n")
        return None
    else:
        print("Unknown error, HTTP Code {}".format(get_resp.http_status))
        return None
    del_resp = RestClientApis.http_delete_and_check_success(doc_url)
    if del_resp.http_status == HTTPStatus.OK:
        return del_resp.json_body
    else:
        return None


