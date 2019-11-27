"""
Common LTI processors for Tahoe.
"""


def basic_user_info(xblock):
    """
    Send basic user information without asking for explicit consent.

    When this processor is used, there's no need for the author to
    manually set the the `ask_to_send_username` and `ask_to_send_email`
    options of the XBlock.

    Legal Notice: The consent should be covered by the Privacy Policy of the site.
    """
    if not callable(xblock.runtime.get_real_user):
        return

    user = xblock.runtime.get_real_user(xblock.runtime.anonymous_student_id)
    return {
        'lis_person_sourcedid': user.username,
        'lis_person_contact_email_primary': user.email,
    }


def personal_user_info(xblock):
    """
    Provide additional standard LTI user personal information.
    """
    if not callable(xblock.runtime.get_real_user):
        return

    user = xblock.runtime.get_real_user(xblock.runtime.anonymous_student_id)
    user_full_name = user.profile.name
    names_list = user_full_name.split(' ', 1)

    params = {
        'lis_person_name_full': user_full_name,
        'lis_person_name_given': names_list[0],
        'custom_user_id': unicode(user.id or ''),  # noqa: F821
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
    try:
        from openedx.core.djangoapps.course_groups import cohorts
    except ImportError:
        return

    if not callable(xblock.runtime.get_real_user):
        return

    user = xblock.runtime.get_real_user(xblock.runtime.anonymous_student_id)
    cohort = cohorts.get_cohort(course_key=xblock.course.id, user=user)

    if cohort and cohort.name:
        return {
            'custom_cohort_name': cohort.name,
            'custom_cohort_id': unicode(cohort.pk),  # noqa: F821
        }


cohort_info.lti_xblock_default_params = {
    'custom_cohort_name': '',
    'custom_cohort_id': '',
}


def team_info(xblock):
    """
    Provide the team information for the current user.
    """
    from django.conf import settings
    features = getattr(settings, 'FEATURES', {})

    if not features.get('ENABLE_TEAMS'):
        return

    # No need for handling ImportError, since `ENABLE_TEAMS` is set to True.
    from lms.djangoapps.teams.models import CourseTeamMembership

    if not callable(xblock.runtime.get_real_user):
        return

    user = xblock.runtime.get_real_user(xblock.runtime.anonymous_student_id)
    try:
        membership = CourseTeamMembership.objects.get(
            user=user,
            team__course_id=xblock.course.id,
        )
    except CourseTeamMembership.DoesNotExist:
        return

    return {
        'custom_team_name': membership.team.name,
        'custom_team_id': unicode(membership.team.team_id),  # noqa: F821
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
