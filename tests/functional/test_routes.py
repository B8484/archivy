from flask.testing import FlaskClient

from responses import RequestsMock, GET
from archivy.extensions import get_max_id


def test_get_index(test_app, client: FlaskClient):
    response = client.get('/')
    assert response.status_code == 200


def test_get_new_bookmark(test_app, client: FlaskClient):
    response = client.get('/bookmarks/new')
    assert response.status_code == 200


def test_post_new_bookmark_missing_fields(test_app, client: FlaskClient):
    response = client.post('/bookmarks/new', data={
        'submit': True
    })
    assert response.status_code == 200
    assert b'This field is required' in response.data

def test_get_new_note(test_app, client: FlaskClient):
    response = client.get('/notes/new')
    assert response.status_code == 200


def test_get_dataobj_not_found(test_app, client: FlaskClient):
    response = client.get('/dataobj/1')
    assert response.status_code == 302


def test_get_dataobj(test_app, client: FlaskClient, note_fixture):
    response = client.get('/dataobj/1')
    assert response.status_code == 200


def test_get_delete_dataobj_not_found(test_app, client: FlaskClient):
    response = client.get('/dataobj/delete/1')
    assert response.status_code == 302


def test_get_delete_dataobj(test_app, client: FlaskClient, note_fixture):
    response = client.get('/dataobj/delete/1')
    assert response.status_code == 302

def test_create_new_bookmark(test_app, client: FlaskClient, mocked_responses: RequestsMock):
    mocked_responses.add(GET, "https://example.com/", body="""<html>
        <head><title>Random</title></head><body><p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit
        </p></body></html>
    """)

    bookmark_data = {
        "url": "https://example.com",
        "tags": "testing,bookmark",
        "desc": "",
        "path": "not classified",
        "submit": "true"
    }

    resp = client.post("/bookmarks/new", data=bookmark_data)
    assert resp.status_code == 302
    assert not b"invalid" in resp.data

    resp = client.post("/bookmarks/new", data=bookmark_data, follow_redirects=True)
    assert resp.status_code == 200
    assert b"testing, bookmark" in resp.data
    assert b"https://example.com" in resp.data
    assert b"Random" in resp.data
    
def test_create_note(test_app, client: FlaskClient):

    note_data = {
        "title": "Testing the create route",
        "tags": "testing,note",
        "desc": "random desc",
        "path": "not classified",
        "submit": "true"
    }


    resp = client.post("/notes/new", data=note_data)
    assert resp.status_code == 302
    assert not b"invalid" in resp.data

    resp = client.post("/notes/new", data=note_data, follow_redirects=True)
    assert resp.status_code == 200
    assert b"testing, note" in resp.data
    assert b"Testing the create route" in resp.data

