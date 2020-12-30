"""
Tests for the xblock_helpers module.
"""
from mock import Mock
import pytest
from django.contrib.auth.models import User
from tahoe_lti.xblock_helpers import get_xblock_user


@pytest.mark.django_db
def test_xblock_with_user():
    """Happy scenario for get_xblock_user"""
    email = 'test@example.com'
    user = User.objects.create(email=email)
    xblock = Mock(runtime=Mock(user_id=user.id))

    fetched_user = get_xblock_user(xblock)
    assert fetched_user.email == email, 'Should return the correct user'


@pytest.mark.django_db
def test_xblock_with_no_user_id():
    """No user_id in the runtime object"""
    xblock = Mock(runtime=object())
    fetched_user = get_xblock_user(xblock)
    assert not fetched_user, 'Should return None if no user id is provided'


@pytest.mark.django_db
def test_xblock_with_incorrect_user_id():
    """Should return None if no user is found"""
    non_existing_user_id = 100000000
    xblock = Mock(runtime=Mock(user_id=non_existing_user_id))
    fetched_user = get_xblock_user(xblock)
    assert not fetched_user, 'Should return None if no user is found'
