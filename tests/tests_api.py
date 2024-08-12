import json
import requests
from jsonschema import validate
from path import path


def test_get_user_list_with_status_code_200(url):
    response = requests.get(url + '/users', params={"page": 2})
    assert response.status_code == 200
    with open(path('get_list_users.json')) as file:
        validate(response.json(), schema=json.loads(file.read()))


def test_post_create_user_with_status_code_201(url):
    response = requests.post(url + '/users', json={"name": "morpheus", "job": "leader"})
    assert response.status_code == 201
    assert response.json()['name'] == 'morpheus'
    assert response.json()['job'] == 'leader'
    with open(path('post_create_user.json')) as file:
        validate(response.json(), schema=json.loads(file.read()))


def test_put_update_user_with_status_code_200(url):
    response = requests.put(url + '/users/2', json={"name": "morpheus", "job": "zion resident"})
    assert response.status_code == 200
    assert response.json()['name'] == 'morpheus'
    assert response.json()['job'] == 'zion resident'
    with open(path('put_update_user.json')) as file:
        validate(response.json(), schema=json.loads(file.read()))


def test_delete_user_with_status_code_204(url):
    response = requests.delete(url + '/users/2')
    assert response.status_code == 204
    assert response.text == ''


def test_get_not_found_singer_user_with_status_code_404(url):
    response = requests.get(url + 'users/23')
    assert response.status_code == 404


def test_post_bad_request_with_status_code_400(url):
    response = requests.post(url + '/login', json={"email": "peter@klaven"})
    assert response.status_code == 400
    assert response.json()['error'] == 'Missing password'
    with open(path('post_login_unsuccessful.json')) as file:
        validate(response.json(), schema=json.loads(file.read()))


def test_positive_post_register_successful(url):
    response = requests.post(url + '/register', json={"email": "eve.holt@reqres.in", "password": "pistol"})
    assert response.status_code == 200
    assert response.json()['id'] == 4
    with open(path('post_register_successful.json')) as file:
        validate(response.json(), schema=json.loads(file.read()))


def test_negative_post_register_unsuccessful(url):
    response = requests.post(url + '/register', json={"email": "sydney@fife"})
    assert response.status_code == 400
    assert response.json()['error'] == 'Missing password'
