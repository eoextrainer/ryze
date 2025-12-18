import importlib


def test_import_app_server():
    m = importlib.import_module('app_server')
    assert hasattr(m, 'app') and m.app is not None
