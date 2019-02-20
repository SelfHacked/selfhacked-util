from selfhacked.iterator.functional import (
    strip, remove_empty, remove_comments,
    decode, split_lines,
)


def test_strip(tmpdir):
    file = tmpdir / '0.txt'
    file.write_text("""123
abc
""", encoding='utf-8')

    with open(str(file)) as f:
        assert tuple(strip(f)) == ('123', 'abc')


def test_remove_empty():
    assert tuple(remove_empty(('123', '', 'abc'))) == ('123', 'abc')


def test_remove_comments():
    assert tuple(remove_comments(('#123', 'abc'))) == ('abc',)


def test_decode():
    assert tuple(decode((b'abc', b'123'))) == ('abc', '123')


def test_split_lines():
    assert tuple(split_lines((
        'abc\n\n123',
        '456\n',
        '789\n'
    ))) == (
               'abc\n',
               '\n',
               '123456\n',
               '789\n'
           )
