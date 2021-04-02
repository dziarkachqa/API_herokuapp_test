from conftest import create_user


def test_authorization(authorized_session):
    session = authorized_session.get("http://127.0.0.1:5000/api/auth/status")
    assert session.json()['description'] == 'authorized as True'


def test_create_database(authorized_session):
    database = authorized_session.request('create', 'http://127.0.0.1:5000/api/create/init')
    assert database.json()['status'] == 'created'


def test_add_user(authorized_session):
    create_user(authorized_session, {'name': 'Anastasia', 'surname': 'Sergeevna', 'sex': 'female', 'grade': 28})
    create_user(authorized_session, {'name': 'Bob', 'surname': 'Bobvich', 'sex': 'male', 'grade': 101})
    create_user(authorized_session, {'name': 'Danila', 'surname': 'Andreevich', 'sex': 'male', 'grade': 9})

    user = authorized_session.get('http://127.0.0.1:5000/api/read/Anastasia')
    assert user.json() == [{'grade': 28, 'id': 1, 'name': 'Anastasia', 'sex': 'female', 'surname': 'Sergeevna'}]


def test_database(authorized_session):
    users_in_database = 0
    database = authorized_session.get('http://127.0.0.1:5000/api/read/all')
    for dic in database:
        users_in_database += 1
    assert users_in_database == 3


def test_change_grade(authorized_session):
    authorized_session.post('http://127.0.0.1:5000/api/update/grade', json={'name': 'Bob', 'grade': 49})
    user = authorized_session.get('http://127.0.0.1:5000/api/read/Bob')
    assert user.json()[0]['grade'] == 49


def test_delete_users(authorized_session):
    authorized_session.request('delete', 'http://127.1.1.0:5000/api/delete/Bob')
    database = authorized_session.get('http://127.0.0.1:5000/api/read/Bob')
    print(database.json())
    assert database.json() == []
