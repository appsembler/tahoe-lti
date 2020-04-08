"""
Helpers to access the XBlock Runtime modules.
"""


def get_xblock_user(xblock):
    """
    Gets the current request user for an XBlock instance.

    :param xblock: XBlock instance.
    :return: User or None.
    """
    from django.contrib.auth import get_user_model
    user_model = get_user_model()

    try:
        user_id = xblock.runtime.user_id
    except AttributeError:
        return

    try:
        return user_model.objects.get(pk=user_id)
    except user_model.DoesNotExist:
        pass
