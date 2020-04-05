import pytest

import csimdjson
from csimdjson import element_type


def test_is_null(parser):
    assert parser.parse("{}").is_null is False
    assert parser.parse("null").is_null is True


def test_json_pointer(parser):
    """Ensure JSON pointers work as expected and all possible exceptions
    are converted to Python types.
    """
    doc = parser.parse('{"key": "value", "array": [0, 1, 2]}')

    assert doc.at('key').type == element_type.STRING
    assert doc.at('array/0').type == element_type.INT64
    assert (doc / 'array' / '0').type == element_type.INT64

    with pytest.raises(csimdjson.NoSuchFieldError):
        doc.at('no_such_key')

    with pytest.raises(csimdjson.IndexOutOfBoundsError):
        doc.at('array/9')

    with pytest.raises(csimdjson.IncorrectTypeError):
        doc.at('array/not_a_num')

    with pytest.raises(csimdjson.InvalidJSONPointerError):
        doc.at('array/')


def test_type_check(parser):
    """Ensures that JSON types are what they say they are."""
    doc = parser.parse('''{
        "array": [],
        "object": {},
        "int64": -1,
        "uint64": 18446744073709551615,
        "double": 1.1,
        "string": "test",
        "bool": true,
        "null_value": null
    }''')

    assert doc['array'].type == element_type.ARRAY
    assert doc['object'].type == element_type.OBJECT
    assert doc['int64'].type == element_type.INT64
    assert doc['uint64'].type == element_type.UINT64
    assert doc['double'].type == element_type.DOUBLE
    assert doc['string'].type == element_type.STRING
    assert doc['bool'].type == element_type.BOOL
    assert doc['null_value'].type == element_type.NULL_VALUE

    assert doc['int64'].up == -1
    assert doc['uint64'].up == 18446744073709551615
    assert doc['double'].up == 1.1
    assert doc['string'].up == 'test'
    assert doc['bool'].up is True
    assert doc['null_value'].up is None


def test_getitem(parser):
    """Ensure accessing a specific element works as expected."""
    doc = parser.parse('''{"key": "value"}''')

    with pytest.raises(KeyError):
        doc['no_such_key']

    assert doc['key']