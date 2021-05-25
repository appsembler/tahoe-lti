"""
Common LTI processors for Tahoe.
"""

import json
from django.conf import settings

from .xblock_helpers import get_xblock_user


DEFAULT_USER_INFO_PARAMS = {
    'lis_person_name_full': '',
    'lis_person_name_given': '',
    'lis_person_name_family': '',
    'custom_user_id': '',
}


def _get_personal_user_info_params(user):
    """
    Return the personal user info params for a user.
    """
    user_full_name = user.profile.name
    names_list = user_full_name.split(' ', 1)

    params = {
        'lis_person_name_full': user_full_name,
        'lis_person_name_given': names_list[0],
        'custom_user_id': str(user.id),
    }

    if len(names_list) > 1:
        params['lis_person_name_family'] = names_list[1]

    return params


def personal_user_info(xblock):
    """
    Provide additional standard LTI user personal information.
    """
    user = get_xblock_user(xblock)
    if not user:
        return {}

    return _get_personal_user_info_params(user)


personal_user_info.lti_xblock_default_params = DEFAULT_USER_INFO_PARAMS


def personal_user_info_with_combined_user_id(xblock):
    """
    Compose a user identification string from user id and join date.

    In rare cases `user.id` cannot be used with LTI providers when the user id
    already exists on the provider side. To support scenarios like this, it is
    needed to have another way to generate a user identification string that
    is unique per user per installation.

    To provide a per-instance unique string for the user, we return the
    combination of the user's id and registration date.
    """
    user = get_xblock_user(xblock)
    if not user:
        return {}

    params = _get_personal_user_info_params(user)
    params['custom_user_id'] = "{user_id}-{date_joined}".format(
        user_id=user.id,
        date_joined=user.date_joined.strftime("%y%m%d%H%M")
    )

    return params


personal_user_info_with_combined_user_id.lti_xblock_default_params = DEFAULT_USER_INFO_PARAMS


def basic_user_info(xblock):
    """
    Send basic user information without asking for explicit consent.

    When this processor is used, there's no need for the author to
    manually set the the `ask_to_send_username` and `ask_to_send_email`
    options of the XBlock.

    Legal Notice: The consent should be covered by the Privacy Policy of the site.
    """
    user = get_xblock_user(xblock)

    if user:
        return {
            'lis_person_sourcedid': user.username,
            'lis_person_contact_email_primary': user.email,
        }
    return {}


def cohort_info(xblock):
    """
    Provide the course cohort information for the current user.
    """
    from .openedx_modules import cohorts

    user = get_xblock_user(xblock)
    if not user:
        return

    cohort = cohorts.get_cohort(course_key=xblock.course.id, user=user)
    if cohort and cohort.name:
        return {
            'custom_cohort_name': cohort.name,
            'custom_cohort_id': str(cohort.pk),
        }


cohort_info.lti_xblock_default_params = {
    'custom_cohort_name': '',
    'custom_cohort_id': '',
}


def team_info(xblock):
    """
    Provide the team information for the current user.
    """
    features = getattr(settings, 'FEATURES', {})
    user = get_xblock_user(xblock)

    if not features.get('ENABLE_TEAMS'):  # Ensure the feature is enabled.
        return
    if not user:  # User should be logged in
        return
    if getattr(xblock.runtime, 'is_author_mode', False):  # Ensure we're in the LMS.
        return

    from .openedx_modules import CourseTeamMembership

    memberships = CourseTeamMembership.objects.filter(
        user=user,
        team__course_id=xblock.course.id,
    )

    if not memberships:
        return

    teams_json = json.dumps([
        {'id': str(membership.team.team_id), 'name': membership.team.name}
        for membership in memberships
    ], sort_keys=True)

    first_membership = memberships[0]  # Support legacy single team per user in Hawthorn
    return {
        'custom_team_name': first_membership.team.name,
        'custom_team_id': str(first_membership.team.team_id),
        'custom_teams': teams_json,
    }


team_info.lti_xblock_default_params = {
    'custom_team_name': '',
    'custom_team_id': '',
    'custom_teams': '[]',
}


def window_document_target(xblock):
    """
    Force the correct Window/IFrame behaviour for LIT Providers who need it like SCORMCloud.
    """
    return {}


window_document_target.lti_xblock_default_params = {
    'launch_presentation_document_target': 'window',
}
