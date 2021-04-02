import pytest
import requests

@pytest.fixture
def authorized_session():
    session = requests.Session()
    session.request('login', 'http://127.0.0.1:5000/api/auth/login',
                               json={'login': 'admin', 'password': 'admin'})
    return session



def create_user(authorized_session, json):
    authorized_session.post('http://127.0.0.1:5000/api/update/add',
                            json=json)