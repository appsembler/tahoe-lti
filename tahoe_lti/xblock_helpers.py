"""
Helpers to access the XBlock Runtime modules.
"""

from django.contrib.auth import get_user_model
User = get_user_model()


def get_xblock_user(xblock):
    """
    Gets the current request user for an XBlock instance.

    :param xblock: XBlock instance.
    :return: User or None.
    """
    try:
        user_id = xblock.runtime.user_id
    except AttributeError:
        return

    try:
        return user_model.objects.get(pk=user_id)
    except user_model.DoesNotExist:
        pass
