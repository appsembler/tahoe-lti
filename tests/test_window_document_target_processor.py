from mock import Mock

from tahoe_lti.processors import window_document_target


def test_window_document_target():
    assert window_document_target(xblock=None) == {}
    assert window_document_target.lti_xblock_default_params == {
        'launch_presentation_document_target': 'window',
    }
