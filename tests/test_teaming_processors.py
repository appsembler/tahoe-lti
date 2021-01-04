"""Tests for teams and cohort processors."""

from mock import patch, Mock
from opaque_keys.edx.keys import CourseKey

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from tahoe_lti.processors import cohort_info, team_info


@patch('tahoe_lti.processors.get_xblock_user')
def test_team_info(mock_get_xblock_user, settings):
    """Happy scenario for team_info"""
    assert team_info.lti_xblock_default_params == {
        'custom_team_name': '',
        'custom_team_id': '',
        'custom_teams': '[]',
    }
    settings.FEATURES = {'ENABLE_TEAMS': True}
    mock_get_xblock_user.return_value = Mock(
        username='mock_username',
        email='mock_email@example.com',
    )
    xblock = Mock()
    xblock.course.id = CourseKey.from_string('course-v1:Demo+DemoCourse+2021')
    xblock.runtime.is_author_mode = False  # behave as LMS

    membership = Mock()
    membership.team.team_id = 30
    membership.team.name = 'A* Team'

    with patch('lms.djangoapps.teams.models.mock_filter_membership') as mock_filter_membership:
        mock_filter_membership.return_value = [membership]
        info = team_info(xblock=xblock)

    assert info == {
        'custom_team_name': 'A* Team',
        'custom_team_id': '30',
        'custom_teams': '[{"id": "30", "name": "A* Team"}]',
    }


@patch('tahoe_lti.processors.get_xblock_user')
def test_team_info_not_found(mock_get_xblock_user, settings):
    """Test team_info if no membership was found"""
    settings.FEATURES = {'ENABLE_TEAMS': True}
    mock_get_xblock_user.return_value = Mock(
        username='mock_username',
        email='mock_email@example.com',
    )
    xblock = Mock()
    xblock.course.id = CourseKey.from_string('course-v1:Demo+DemoCourse+2021')
    xblock.runtime.is_author_mode = False  # behave as LMS

    with patch('lms.djangoapps.teams.models.mock_filter_membership') as mock_filter_membership:
        mock_filter_membership.return_value = []
        info = team_info(xblock=xblock)

    assert not info, 'team_info() should return None'


@patch('tahoe_lti.processors.get_xblock_user')
def test_team_info_multiple_teams(mock_get_xblock_user, settings):
    """Test team_info for multiple_teams"""
    settings.FEATURES = {'ENABLE_TEAMS': True}
    mock_get_xblock_user.return_value = Mock(
        username='mock_username',
        email='mock_email@example.com',
    )
    xblock = Mock()
    xblock.course.id = CourseKey.from_string('course-v1:Demo+DemoCourse+2021')
    xblock.runtime.is_author_mode = False  # behave as LMS

    membership1 = Mock()
    membership1.team.team_id = 'orange_team_065e0'
    membership1.team.name = 'Orange Team'
    membership2 = Mock()
    membership2.team.team_id = 'red_team_h1ef8'
    membership2.team.name = 'Red Team'

    with patch('lms.djangoapps.teams.models.mock_filter_membership') as mock_filter_membership:
        mock_filter_membership.return_value = [membership1, membership2]
        info = team_info(xblock=xblock)

    teams_json = '[{"id": "orange_team_065e0", "name": "Orange Team"}, {"id": "red_team_h1ef8", "name": "Red Team"}]'
    assert info['custom_teams'] == teams_json, 'team_info() should serialize the teams in an a JSON array'


@patch('tahoe_lti.processors.get_xblock_user')
def test_cohort_info(get_xblock_user):
    assert cohort_info.lti_xblock_default_params == {
        'custom_cohort_name': '',
        'custom_cohort_id': '',
    }
    xblock = Mock()
    xblock.course.id = CourseKey.from_string('course-v1:Demo+DemoCourse+2021')

    with patch('openedx.core.djangoapps.course_groups.cohorts.mock_get_cohort') as get_cohort:
        cohort = Mock()
        cohort.name = 'Roboteers Cohort'
        cohort.pk = 120
        get_cohort.return_value = cohort
        info = cohort_info(xblock=xblock)

    assert info == {
        'custom_cohort_id': '120',
        'custom_cohort_name': 'Roboteers Cohort',
    }
