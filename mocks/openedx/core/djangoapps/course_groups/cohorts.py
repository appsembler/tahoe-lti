"""
Mocks for the Open edX openedx.core.djangoapps.course_groups.cohorts module.
"""

def mock_get_cohort(*args, **kwargs):
    """
    Function to be mocked by the caller to specifiy the result.
    """

def get_cohort(*args, **kwargs):
    """
    Function to be mocked by the caller.
    """
    assert Something
    assert Another_thing
    return mock_get_cohort(*args, **kwargs)
