#! /usr/bin/env python3

"""
CouchDB REST APIs
"""
import json
from http import HTTPStatus
from json import JSONDecodeError
from magen_rest_apis.rest_client_apis import RestClientApis
from requests.exceptions import ChunkedEncodingError

__author__ = "rapenno@gmail.com"
__copyright__ = "Copyright(c) 2018, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"
__license__ = "Apache"

# TODO Replace print by logs


def create_db(url, db_name, overwrite=False):
    """
    Creates a DB in couchDB. We return success if db was created or already exists.
    :param overwrite: whether to overwrite db if it exists
    :param url: couchDB base URL in format http://host:port/
    :param db_name:  name of db to be created
    :return: boolean
    """
    if overwrite:
        delete_db(url, db_name)
    put_resp = RestClientApis.http_put_and_check_success(url + db_name, "{}")
    if put_resp.http_status == HTTPStatus.CREATED or \
            put_resp.http_status == HTTPStatus.PRECONDITION_FAILED:
        return 0
    else:
        print("Failed to create DB {}".format(url + db_name))
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
        print("Failed to delete DB {}".format(url + db_name))
        return -1


def create_named_document(url: str, db_name: str, doc_name: str, document: str, overwrite=False) -> dict or None:
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
            # If document does not exist we continue and add it
            print("Overwrite requested but document does not exist \n")
        elif get_resp.http_status == HTTPStatus.UNAUTHORIZED:
            print("Overwrite requested but not enough permissions \n")
            return None
        else:
            print("Error reading doc_id {}. HTTP Code {}".
                  format(doc_url, get_resp.http_status))
            return None
    put_resp = RestClientApis.http_put_and_check_success(doc_url, document)
    if put_resp.http_status == HTTPStatus.CREATED:
        return put_resp.json_body
    else:
        print("Failed to save doc_id {}, doc {}. HTTP Code: {}".
              format(doc_url, document, put_resp.http_status))
        return None


def get_named_document(url: str, db_name: str, doc_name: str) -> dict or None:
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
        print("Failed to read doc_id {}. HTTP Code: {}".
              format(doc_url, get_resp.http_status))
        return None


def get_db_all_docs(url: str, db_name: str) -> list or None:
    """
    Retrieve all docs for a DB. CouchDB returns list of documents as
    chunked-encoding, therefore special reassembly is needed
    :param url: CouchDB URL
    :param db_name: DB name
    :return: A list of JSON dicts objects
    """

    # Make static analysis happy
    buf = None
    try:
        json_dict_list = list()
        all_docs = url + db_name + "/" + "_all_docs"
        get_resp = RestClientApis.http_get_and_check_success(all_docs)
        headers = get_resp.response_object.headers
        if ("Transfer-Encoding", "chunked") in headers.items():
            for buf in read_chunks(get_resp.response_object):
                json_dict = json.loads(buf)
                json_dict_list.append(json_dict)
            return json_dict_list
        else:
            return None
    except JSONDecodeError:
        error_msg = "Error decoding response {}".format(buf)
        print(error_msg)
        return None


def read_chunks(resp) -> str:
    """
    We iterate over chunks, reassemble and return them.
    :param resp: A requests response object
    :return: decoded chunk
    """
    buf = ""
    try:
        for chunk in resp.iter_content(chunk_size=None):
            if chunk.endswith(b"\n"):
                buf += chunk.decode("utf-8")
                yield buf
                buf = ""
            else:
                buf += chunk
    except ChunkedEncodingError as e:
        # Nothing to do, connection terminated.
        pass


def delete_named_document(url: str, db_name: str, doc_name: str) -> dict or None:
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
        print("Error reading doc_id {}. HTTP Code {}".
              format(doc_url, get_resp.http_status))
        return None
    del_resp = RestClientApis.http_delete_and_check_success(doc_url)
    if del_resp.http_status == HTTPStatus.OK:
        return del_resp.json_body
    else:
        print("Error deleting doc_id {}. HTTP Code {}".
              format(doc_url, get_resp.http_status))
        return None


