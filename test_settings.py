"""
Settings for the tests.
"""

from os.path import abspath, dirname, join
import sys

from workbench.settings import *  # Using the XBlock generic settings for a shorter settings file

from django.conf.global_settings import LOGGING  # Fix "file not found" with the workbench.settings LOGGING config


def root(*args):
    """
    Get the absolute path of the given path relative to the project root.
    """
    return join(abspath(dirname(__file__)), *args)


sys.path.append(root('mocks'))
