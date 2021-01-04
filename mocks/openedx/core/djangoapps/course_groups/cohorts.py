"""
Mocks for the Open edX openedx.core.djangoapps.course_groups.cohorts module.
"""

from opaque_keys.edx.keys import CourseKey


def mock_get_cohort(*args, **kwargs):
    """
    Function to be mocked by the caller to specify the result.
    """
    raise RuntimeError('Please @patch mock_get_cohort and provide a return value.')


def get_cohort(course_key, user):
    """
    Function to be mocked by the caller.
    """
    assert isinstance(course_key, CourseKey), 'Needs a course key'
    return mock_get_cohort(course_key, user)
