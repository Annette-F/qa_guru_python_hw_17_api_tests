import json
import requests
from jsonschema import validate
from path import path


def test_get_user_list(url):
    response = requests.get(url + '/users', params={"page": 2})
    with open(path('get_list_users.json')) as file:
        validate(response.json(), schema=json.loads(file.read()))
    assert response.status_code == 200
    assert response.json()['page'] == 2


def test_post_create_user(url):
    response = requests.post(url + '/users', json={"name": "morpheus", "job": "leader"})
    with open(path('post_create_user.json')) as file:
        validate(response.json(), schema=json.loads(file.read()))
    assert response.status_code == 201
    assert response.json()['name'] == 'morpheus'
    assert response.json()['job'] == 'leader'


def test_put_update_user(url):
    response = requests.put(url + '/users/2', json={"name": "morpheus", "job": "zion resident"})
    with open(path('put_update_user.json')) as file:
        validate(response.json(), schema=json.loads(file.read()))
    assert response.status_code == 200
    assert response.json()['name'] == 'morpheus'
    assert response.json()['job'] == 'zion resident'


def test_delete_user(url):
    response = requests.delete(url + '/users/2')
    assert response.status_code == 204
    assert response.text == ''


def test_get_not_found_singer_user(url):
    response = requests.get(url + '/users/23')
    assert response.status_code == 404
    assert response.json() == {}


def test_post_bad_request(url):
    response = requests.post(url + '/login', json={"email": "peter@klaven"})
    with open(path('post_login_unsuccessful.json')) as file:
        validate(response.json(), schema=json.loads(file.read()))
    assert response.status_code == 400
    assert response.json()['error'] == 'Missing password'


def test_positive_post_register_successful(url):
    response = requests.post(url + '/register', json={"email": "eve.holt@reqres.in", "password": "pistol"})
    with open(path('post_register_successful.json')) as file:
        validate(response.json(), schema=json.loads(file.read()))
    assert response.status_code == 200
    assert response.json()['id'] == 4


def test_negative_post_register_unsuccessful(url):
    response = requests.post(url + '/register', json={"email": "sydney@fife"})
    assert response.status_code == 400
    assert response.json()['error'] == 'Missing password'
