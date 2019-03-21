import pytest

from selfhacked.csv.field import ArrayField, TextField, ListField, IntegerField, FloatField


@pytest.mark.dependency(
    depends=[
        ('session', 'tests/csv/test_field_basic.py::test_text_field'),
    ],
)
def test_array_field():
    field = ArrayField(
        TextField(),
        delimiters=[','],
    )
    assert field.parse('a') == ['a']
    assert field.parse('a,b') == ['a', 'b']


@pytest.mark.dependency(
    depends=[
        'test_array_field',
        ('session', 'tests/csv/test_field_basic.py::test_text_field'),
    ],
)
def test_multiple_delimiters():
    field = ArrayField(
        TextField(),
        delimiters=[',', ';'],
    )
    assert field.parse('a,b;c') == ['a', 'b', 'c']


@pytest.mark.dependency(
    depends=[
        'test_array_field',
        ('session', 'tests/csv/test_field_basic.py::test_text_field'),
    ],
)
def test_strip_column():
    field1 = ArrayField(
        TextField(),
        delimiters=[','],
    )
    assert field1.parse('a, b') == ['a', 'b']

    field2 = ArrayField(
        TextField(),
        delimiters=[','],
        strip_columns=False,
    )
    assert field2.parse('a, b') == ['a', ' b']


def test_array_length():
    assert ArrayField.array_length(None) == 0
    assert ArrayField.array_length([]) == 0
    assert ArrayField.array_length([1, 2]) == 2


@pytest.mark.dependency(
    depends=[
        ('session', 'tests/csv/test_field_basic.py::test_numeric'),
    ],
)
def test_list_field():
    field = ListField(
        [IntegerField(), FloatField()],
        delimiters=[';'],
    )
    assert field.parse('1;23.4') == [1, 23.4]
    with pytest.raises(IntegerField.ParseError):
        assert field.parse('1.5;2')


@pytest.mark.dependency(
    depends=[
        'test_list_field',
        ('session', 'tests/csv/test_field_basic.py::test_text_field'),
    ],
)
def test_max_split():
    field = ListField(
        [TextField(), TextField()],
        delimiters=[','],
        max_split=1,
    )
    assert field.parse('1,2,3') == ['1', '2,3']


@pytest.mark.dependency(
    depends=[
        'test_list_field',
        'test_max_split',
        ('session', 'tests/csv/test_field_basic.py::test_text_field'),
        ('session', 'tests/csv/test_field_basic.py::test_numeric'),
    ],
)
def test_from_right():
    field = ListField(
        [IntegerField(), TextField()],
        delimiters=['-'],
        from_right=True,
        max_split=1,
    )
    assert field.parse('x-1') == [1, 'x']
    assert field.parse('x-b-1') == [1, 'x-b']
