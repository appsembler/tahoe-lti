"""
A module to collect all Open edX imports in a single place.

The module aims to list all imports explicitly until proper `api.py` is
developed in Open edX for this plugin.
"""

from openedx.core.djangoapps.course_groups import cohorts  # noqa
from lms.djangoapps.teams.models import CourseTeamMembership  # noqa
