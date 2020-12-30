from mock import patch, Mock

from tahoe_lti.processors import basic_user_info


@patch('tahoe_lti.processors.get_xblock_user')
def test_basic_user_info(mock_get_xblock_user):
    """Happy scenario for test_basic_user_info"""
    mock_get_xblock_user.return_value = Mock(
        username='mock_username',
        email='mock_email@example.com',
    )
    assert basic_user_info(xblock=None) == {
        'lis_person_sourcedid': 'mock_username',
        'lis_person_contact_email_primary': 'mock_email@example.com',
    }
    assert not hasattr(basic_user_info, 'lti_xblock_default_params')
