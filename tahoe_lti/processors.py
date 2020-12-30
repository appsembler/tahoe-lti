"""
Common LTI processors for Tahoe.
"""

from django.conf import settings

from .xblock_helpers import get_xblock_user


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


def personal_user_info(xblock):
    """
    Provide additional standard LTI user personal information.
    """
    user = get_xblock_user(xblock)
    if not user:
        return

    user_full_name = user.profile.name
    names_list = user_full_name.split(' ', 1)

    params = {
        'lis_person_name_full': user_full_name,
        'lis_person_name_given': names_list[0],
        'custom_user_id': str(user.id or ''),
    }

    if len(names_list) > 1:
        params['lis_person_name_family'] = names_list[1]

    return params


personal_user_info.lti_xblock_default_params = {
    'lis_person_name_full': '',
    'lis_person_name_given': '',
    'lis_person_name_family': '',
    'custom_user_id': '',
}


def cohort_info(xblock):
    """
    Provide the course cohort information for the current user.
    """
    from .openedx import cohorts

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

    from .openedx import CourseTeamMembership

    try:
        membership = CourseTeamMembership.objects.get(
            user=user,
            team__course_id=xblock.course.id,
        )
    except CourseTeamMembership.DoesNotExist:
        return

    return {
        'custom_team_name': membership.team.name,
        'custom_team_id': str(membership.team.team_id),
    }


team_info.lti_xblock_default_params = {
    'custom_team_name': '',
    'custom_team_id': '',
}


def window_document_target(xblock):
    """
    Force the correct Window/IFrame behaviour for LIT Providers who need it like SCORMCloud.
    """
    return {}


window_document_target.lti_xblock_default_params = {
    'launch_presentation_document_target': 'window',
}
