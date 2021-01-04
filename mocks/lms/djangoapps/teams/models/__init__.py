"""
Mocks for the Open edX lms.djangoapps.teams.models module.
"""

from mock import Mock
from opaque_keys.edx.keys import CourseKey

CourseTeamMembership = Mock()


def mock_get_membership(*args, **kwargs):
    """
    Function to be @patch'ed.
    """
    raise RuntimeError('Please @patch mock_get_membership')


def course_team_membership_objects_get(user, team__course_id):
    """
    Actual called in the `CourseTeamMembership` mock.
    """
    assert isinstance(team__course_id, CourseKey), 'Needs a course key'
    return mock_get_membership(user, team__course_id)


CourseTeamMembership.objects.get = course_team_membership_objects_get
CourseTeamMembership.DoesNotExist = RuntimeError