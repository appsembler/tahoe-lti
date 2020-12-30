"""
Mocks for the Open edX lms.djangoapps.teams.models module.
"""

from mock import Mock


CourseTeamMembership = Mock()


def mock_course_team_membership_objects_get(*args, **kwargs):
    """
    Function to be @patch'ed.
    """
    raise RuntimeError('Please @patch mock_course_team_membership_objects_get')


def course_team_membership_objects_get(*args, **kwargs):
    """
    Actual called in the `CourseTeamMembership` mock.
    """
    assert Something
    assert Another_thing
    return mock_course_team_membership_objects_get(*args, **kwargs)


CourseTeamMembership.objects.get = course_team_membership_objects_get
