import pytest

from selfhacked.csv.schema import CsvSchema


def test_setup_error():
    with pytest.raises(CsvSchema.SetupError):
        schema = CsvSchema(header=False, replace_header={'X': 'x'})
    with pytest.raises(CsvSchema.SetupError):
        schema = CsvSchema(header=False, as_dict=True)


def test_read_header():
    schema = CsvSchema()
    assert schema.header is None
    assert schema.read_line('a,b') is None
    assert schema.header == ('a', 'b')


def test_provide_header():
    schema = CsvSchema(header=['a', 'b'])
    assert schema.header == ('a', 'b')
    schema.read_line('1,2')
    assert schema.header == ('a', 'b')


def test_no_header():
    schema = CsvSchema(header=False)
    assert schema.header is None
    schema.read_line('1,2')
    assert schema.header is None


def test_replace_header():
    schema = CsvSchema(header=True, replace_header={'X': 'x'})
    schema.read_line('X,y')
    assert schema.header == ('x', 'y')


def test_read_list():
    schema = CsvSchema(header=False)
    assert schema.read_line('1,2') == ['1', '2']


@pytest.mark.depenedency(
    depends=['test_provide_header'],
)
def test_read_dict():
    schema = CsvSchema(
        header=['a', 'b'],
        as_dict=True,
    )
    assert schema.read_line('1,2') == {'a': '1', 'b': '2'}
    assert schema.read_line('3') == {'a': '3', 'b': None}


@pytest.mark.dependency(
    depends=[
        'test_read_header',
        'test_read_list',
    ],
)
def test_read_file():
    schema = CsvSchema()
    file = [
        'a,b',
        '1,2',
        '3,4',
    ]
    rows = schema.read_file(file)
    assert next(rows) == ['1', '2']
    assert schema.header == ('a', 'b')
    assert next(rows) == ['3', '4']
    with pytest.raises(StopIteration):
        next(rows)


def test_lineno():
    schema = CsvSchema()
    assert schema.lineno == -1
    schema.read_line('a,b')
    assert schema.lineno == 0
    schema.read_line('1,2')
    assert schema.lineno == 1
    schema.reset()
    assert schema.lineno == -1
