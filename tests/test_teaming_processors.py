"""Tests for teams and cohort processors."""

from mock import patch, Mock
from opaque_keys.edx.keys import CourseKey

from tahoe_lti.processors import cohort_info, team_info


@patch('tahoe_lti.processors.get_xblock_user')
def test_team_info(mock_get_xblock_user, settings):
    """Happy scenario for team_info"""
    assert team_info.lti_xblock_default_params == {
        'custom_team_name': '',
        'custom_team_id': '',
    }
    settings.FEATURES = {'ENABLE_TEAMS': True}
    mock_get_xblock_user.return_value = Mock(
        username='mock_username',
        email='mock_email@example.com',
    )
    xblock = Mock()
    xblock.course.id = CourseKey.from_string('course-v1:Demo+DemoCourse+2021')
    xblock.runtime.is_author_mode = False  # behave as LMS

    with patch('lms.djangoapps.teams.models.mock_get_membership') as mock_get_membership:
        membership = Mock()
        membership.team.team_id = 30
        membership.team.name = 'A* Team'
        mock_get_membership.return_value = membership
        info = team_info(xblock=xblock)

    assert info == {
        'custom_team_name': 'A* Team',
        'custom_team_id': '30',
    }


@patch('tahoe_lti.processors.get_xblock_user')
def test_cohort_info(mock_get_xblock_user, settings):
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
