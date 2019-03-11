import pytest

from selfhacked.csv.field import (
    Field,
    TextField,
    IntegerField,
    FloatField,
    BoolField,
    ChoiceField,
    CleanTextField,
)


def test_empty():
    field = Field()
    assert field.parse(None) is None
    assert field.parse('') is None


def test_not_implemented():
    field = Field()
    with pytest.raises(NotImplementedError):
        assert field.parse('abc')


def test_type():
    field1 = Field(type=str)
    assert field1.parse('abc') == 'abc'
    field2 = Field(type=int)
    assert field2.parse('1') == 1


@pytest.mark.dependency(
    depends=[
        'test_type',
    ],
)
def test_none():
    field = Field(
        none={'N/A'},
        type=int,
    )
    assert field.parse('N/A') is None
    assert field.parse('1') == 1


@pytest.mark.dependency(
    depends=[
        'test_type',
        'test_empty',
        'test_none',
    ],
)
def test_str_replace():
    field = TextField(
        none='x',
        str_replace={'-': ''},
        type=str,
    )
    assert field.parse('---') is None
    assert field.parse('a-b') == 'ab'
    assert field.parse('-x-') is None


def test_text_field():
    field = TextField()
    assert field.parse('abc') == 'abc'


def test_numeric():
    int_field = IntegerField()
    assert int_field.parse('1') == 1
    with pytest.raises(IntegerField.ParseError):
        int_field.parse('x')

    float_field = FloatField()
    assert float_field.parse('1.5') == 1.5
    with pytest.raises(FloatField.ParseError):
        float_field.parse('x')


@pytest.mark.dependency(
    depends=['test_numeric'],
)
def test_numeric_comma():
    int_field = IntegerField(comma=True)
    assert int_field.parse('1,234') == 1234

    float_field = FloatField(comma=True)
    assert float_field.parse('1,234.56') == 1234.56


def test_bool_field():
    field = BoolField(
        true={'1', 'true'},
        false={'0', 'false'},
    )
    assert field.parse('1') is True
    assert field.parse('true') is True
    assert field.parse('0') is False
    assert field.parse('false') is False
    with pytest.raises(BoolField.ParseError):
        field.parse('2')


def test_choice_field():
    field = ChoiceField(
        {'1', '2', 'abc'},
        type=str,
    )
    assert field.parse('1') == '1'
    assert field.parse('2') == '2'
    assert field.parse('abc') == 'abc'
    with pytest.raises(ChoiceField.ParseError):
        field.parse('a')


def test_clean_text_field():
    field = CleanTextField(
        allowed='abcdefg',
    )
    assert field.parse('acf') == 'acf'
    with pytest.raises(CleanTextField.ParseError):
        field.parse('h')


def test_clean_text_field_no_error():
    field = CleanTextField(
        allowed='abcdefg',
        raise_=False,
    )
    assert field.parse('acf') == 'acf'
    assert field.parse('h') == 'h'
