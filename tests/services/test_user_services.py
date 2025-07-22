import pytest
from app.services.user_service import UserService
from app.exceptions import UserValidationError, AuthenticationError, NotFoundError
from app.models import User


def test_create_user_success(db):
    user = UserService.create_user('alice', 'alice@example.com', 'strongpass123')
    assert user.id is not None
    assert user.username == 'alice'
    assert user.email == 'alice@example.com'


def test_create_user_missing_fields():
    with pytest.raises(UserValidationError):
        UserService.create_user(None, 'bob@example.com', 'password123')
    with pytest.raises(UserValidationError):
        UserService.create_user('bob', None, 'password123')
    with pytest.raises(UserValidationError):
        UserService.create_user('bob', 'bob@example.com', None)


def test_create_user_duplicate(db):
    UserService.create_user('charlie', 'charlie@example.com', 'password123')
    with pytest.raises(UserValidationError):
        UserService.create_user('charlie', 'charlie@example.com', 'password123')


def test_authenticate_success(db):
    UserService.create_user('dave', 'dave@example.com', 'password1234')
    token = UserService.authenticate('dave@example.com', 'password1234')
    assert isinstance(token, str) and token


def test_authenticate_invalid_credentials():
    with pytest.raises(AuthenticationError):
        UserService.authenticate('noone@example.com', 'wrongpass')


def test_get_user_by_id_success(db):
    user = UserService.create_user('eve', 'eve@example.com', 'password123')
    fetched = UserService.get_user_by_id(user.id)
    assert fetched.id == user.id


def test_get_user_by_id_not_found():
    with pytest.raises(NotFoundError):
        UserService.get_user_by_id(9999)