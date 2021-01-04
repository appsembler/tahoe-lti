"""
Mocks for the Open edX lms.djangoapps.teams.models module.
"""

from mock import Mock
from opaque_keys.edx.keys import CourseKey

from django.core.exceptions import ObjectDoesNotExist

CourseTeamMembership = Mock()


def mock_filter_membership(*args, **kwargs):
    """
    Function to be @patch'ed.
    """
    raise RuntimeError('Please @patch mock_filter_membership')


def course_team_membership_objects_filter(user, team__course_id):
    """
    Actual called in the `CourseTeamMembership` mock.
    """
    assert isinstance(team__course_id, CourseKey), 'Needs a course key'
    return mock_filter_membership(user, team__course_id)


CourseTeamMembership.objects.filter = course_team_membership_objects_filter
CourseTeamMembership.DoesNotExist = ObjectDoesNotExist
