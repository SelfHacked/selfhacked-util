import pytest

from selfhacked.csv.field import IntegerField, Field, ArrayField, ListField, TextField


def test_parent():
    field1 = Field()
    field2 = IntegerField(parent=field1)
    assert field2.parent == field1
    with pytest.raises(Field.SetupError):
        field2.parent = None
    field2.parent = field1
    assert field2.parent == field1

    array = ArrayField(
        field1,
        delimiters=[','],
    )
    assert field1.parent == array

    field3 = IntegerField()
    li = ListField(
        [array, field3],
        delimiters=[';'],
    )
    assert array.parent == li
    assert field3.parent == li


def test_name():
    field1 = IntegerField()
    array = ArrayField(
        field1,
        delimiters=[','],
    )
    array.name = 'arr'
    assert array.name == 'arr'
    assert field1.name == 'arr[]'

    field2 = IntegerField()
    li = ListField(
        [field2],
        delimiters=[','],
    )
    li.name = 'li'
    assert li.name == 'li'
    assert field2.name == 'li[0]'

    field3 = IntegerField(name='int')
    assert field3.name == 'int'
    field3.name = 'x'
    assert field3.name == 'int'


def test_type_name():
    assert IntegerField().type_name == 'IntegerField'
    assert ArrayField(
        IntegerField(),
        delimiters=[','],
    ).type_name == 'ArrayField[IntegerField]'
    assert ListField(
        [IntegerField(), TextField()],
        delimiters=[','],
    ).type_name == 'ListField[IntegerField, TextField]'
