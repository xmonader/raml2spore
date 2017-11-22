import pytest
import raml2spore
import sys
import os.path


modpath = sys.modules[__name__].__file__

RAML_FILE = os.path.join(os.path.dirname(modpath), "api.raml")

print(RAML_FILE)


def test_raml_load_from_string():
    with open(RAML_FILE) as f:
        source = f.read()
        assert raml2spore.raml_from_string(source) is not None


def test_raml_load_from_file():
    assert raml2spore.raml_from_file(RAML_FILE) is not None
