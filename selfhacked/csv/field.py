import time

import logging
import string
from logging import Logger
from typing import List, Collection, Sequence, Dict, Type, Any, Tuple, Iterable, Union, Optional

from selfhacked.util.func import returns
from .schema import CsvSchema

RAISE = logging.CRITICAL + 10

logger_module = logging.getLogger(__name__)


class Field(object):
    """
    A base field used in CsvFieldSchema
    """

    class SetupError(Exception):
        pass

    class ParseError(ValueError):
        """
        Don't raise directly; use self._raise instead
        """

        def __init__(self, msg: tuple, prepared_msg: str):
            self.msg = msg
            super().__init__(prepared_msg)

    NONE = None
    WARN = {'NA', 'NR'}
    STR_REPLACE = None
    REPLACE = None
    TYPE = None
    RAISE = True

    def __init__(
            self,
            *,
            parent: 'Field' = None,
            name: str = None,
            none: Collection[str] = None,
            warn: Collection[str] = None,
            str_replace: Dict[str, str] = None,
            replace: Dict[str, Any] = None,
            type: Type = None,
            raise_: bool = None,
    ):
        """
        :param parent:
            Parent field, if any.
            Only needed when creating custom fields that have children.
        :param name:
            Give name.
            If None, name will be extracted from schema.
        :param none:
            A collection of strings that should be treated as None.
        :param warn:
            A collection of strings which,
            if the pre-parse value matches one of them,
            will send a warning.
        :param str_replace:
            Replace substrings.
        :param replace:
            Replace whole string to a value.
        :param type:
            Data type.
        :param raise_:
            If True (default), raise error;
            If False, log error instead.
        """

        self.__schema: 'CsvFieldSchema' = None
        self.__parent: 'Field' = parent
        self.__name = name
        self.__name_set = None

        self.__none = self._option('none', none, nullable=True, type=set)
        self.__warn = self._option('warn', warn, nullable=True, type=set)
        self.__str_replace = self._option('str_replace', str_replace, nullable=True, type=dict)
        self.__replace = self._option('replace', replace, nullable=True, type=dict)
        self.__type = self._option('type', type, nullable=True)
        self.__raise = self._option('raise', raise_, type=bool)

        self.__unique_logs = set()

    @property
    def schema(self) -> 'CsvFieldSchema':
        return self.__schema

    @schema.setter
    def schema(self, val: 'CsvFieldSchema'):
        self.__schema = val
        self._set_children_schema(val)

    def _set_children_schema(self, val: 'CsvFieldSchema'):
        pass

    @property
    def parent(self) -> 'Field':
        return self.__parent

    @parent.setter
    def parent(self, val: 'Field'):
        if self.__parent is not None:
            if self.__parent != val:
                raise self.SetupError('Cannot have two parents')
            return
        self.__parent = val

    @property
    def name(self) -> str:
        if self.__name is not None:
            return self.__name
        return self.__name_set

    @name.setter
    def name(self, val: str):
        if self.__name is None:
            self.__name_set = val
        self._set_children_name(val)

    def _set_children_name(self, val: str):
        pass

    @property
    def type_name(self) -> str:
        return self.__class__.__name__

    @property
    def _logger(self) -> Optional[Logger]:
        if self.schema is None:
            return None
        return self.schema.logger

    def __prepare_log_msg(self, *msg, unique: bool):
        msg = tuple(
            str(m)
            for m in msg
        )
        if self.schema is None:
            return msg, '\t'.join(msg)
        else:
            context = self.schema.context
            return msg, '\t'.join((
                str(context['lineno']),
                '[uniq]' if unique else '[all]',
                context['field'],
                context['value'],
                self.name,
                *msg,
            ))

    def __log(self, msg: tuple, prepared_msg: str, *, level, unique: bool):
        if level >= RAISE:
            raise self.ParseError(msg, prepared_msg)
        if self._logger is None:
            return
        if not unique:
            self._logger.log(level, prepared_msg)
            return
        if (level, msg) in self.__unique_logs:
            return
        self.__unique_logs.add((level, msg))
        self._logger.log(level, prepared_msg)

    def _log(
            self,
            *msg,
            level,
            unique=False,
    ):
        msg, prepared_msg = self.__prepare_log_msg(*msg, unique=unique)
        self.__log(msg, prepared_msg, level=level, unique=unique)

    def _info(self, *msg, unique=False):
        self._log(
            *msg,
            level=logging.INFO,
            unique=unique,
        )

    def _warn(self, *msg, unique=False):
        self._log(
            *msg,
            level=logging.WARNING,
            unique=unique,
        )

    def _error(self, *msg, unique=False):
        self._log(
            *msg,
            level=logging.ERROR,
            unique=unique,
        )

    def _raise(self, *msg):
        self._log(
            *msg,
            level=RAISE,
        )

    def _option(
            self,
            name: str,
            opt,
            *,
            nullable=False,
            type=None,
    ):
        if opt is not None:
            if type is not None:
                opt = type(opt)
            return opt
        default = getattr(self, name.upper())
        if default is not None:
            if type is not None:
                default = type(default)
            return default
        if nullable:
            return None
        raise self.SetupError(f"Option `{name}` not provided")

    def _is_none(self, s: str) -> bool:
        if self.__none is None:
            return False
        return s in self.__none

    def _str_replace(self, s: str) -> str:
        if self.__str_replace is None:
            return s
        for k, v in self.__str_replace.items():
            s = s.replace(k, v)
        return s

    def _replace(self, s: str) -> Any:
        if self.__replace is None:
            return s
        if s in self.__replace:
            s = self.__replace[s]
        return s

    def _validate_pre(self, s: str):
        if self.__warn is None:
            return
        if s in self.__warn:
            self._warn(s, 'invalid value found', unique=True)

    def _validate_post(self, val):
        pass

    @property
    def raises(self) -> bool:
        return self.__raise

    def __parse(self, s: str):
        s = self._str_replace(s)
        if not s:
            return None
        if self._is_none(s):
            return None
        s = self._replace(s)
        self._validate_pre(s)
        try:
            val = self._parse(s)
        except NotImplementedError:
            raise
        except self.ParseError:
            raise
        except Exception as e:
            return self._raise(s, e)
        self._validate_post(val)
        return val

    def parse(self, s: str):
        try:
            return self.__parse(s)
        except NotImplementedError:
            raise
        except self.ParseError as e:
            if self.raises:
                raise
            self._error(*e.msg)
            return None

    def _parse(self, s: str):
        if self.__type is None:
            raise NotImplementedError
        return self.__type(s)


class DelimitedField(Field):
    DELIMITERS = None
    STRIP_COLUMNS = True

    TYPE = list

    def __init__(
            self,
            *,
            delimiters: Collection[str] = None,
            strip_columns: bool = None,
            **kwargs,
    ):
        super().__init__(**kwargs)

        self.__delimiters = self._option('delimiters', delimiters, type=tuple)

        self.__strip_columns = self._option('strip_columns', strip_columns, type=bool)

    @property
    def _delimiters(self) -> Tuple[str]:
        return self.__delimiters

    def _split(self, s: str) -> Iterable[str]:
        for i in range(len(s)):
            sub = s[i:]
            for delimiter in self._delimiters:
                if not sub.startswith(delimiter):
                    continue
                a = s[:i]
                b = s[i + len(delimiter):]
                yield a
                yield from self._split(b)
                return
        yield s

    def _strip(self, items: Iterable[str]) -> List[str]:
        if not self.__strip_columns:
            return list(items)
        return [
            item.strip()
            for item in items
        ]

    def _parse(self, s: str):
        items = self._split(s)
        items = self._strip(items)
        return items


class ArrayField(DelimitedField):
    """
    A field that is an array of underlying fields that have the same type
    """

    def __init__(
            self,
            field: Field,
            **kwargs,
    ):
        super().__init__(**kwargs)
        self.__field = field
        self.__field.parent = self

    def _set_children_schema(self, val: 'CsvFieldSchema'):
        self.__field.schema = val

    def _set_children_name(self, val: str):
        self.__field.name = f"{val}[]"

    @property
    def type_name(self) -> str:
        return f"{super().type_name}[{self.__field.type_name}]"

    def _parse(self, s: str):
        return [
            self.__field.parse(item)
            for item in super()._parse(s)
        ]


class ListField(DelimitedField):
    """
    A field that is a list of underlying fields that have different types
    """

    MAX_SPLIT = None
    FROM_RIGHT = False

    def __init__(
            self,
            fields: Sequence[Field],
            *,
            max_split: int = None,
            from_right: bool = None,
            **kwargs,
    ):
        """
        :param fields: A list of fields
        :param max_split:
        :param from_right:
            By default (False), split from the left.
            If True, split from the right and *reverse the order*,
            so the rightmost substring will be parsed by the first child field.
        :param kwargs: See base classes
        """

        super().__init__(**kwargs)
        self.__fields = tuple(fields)
        for field in self.__fields:
            field.parent = self

        self.__max_split = self._option('max_split', max_split, nullable=True, type=int)
        self.__from_right = self._option('from_right', from_right, type=bool)

    def __split_left(self, s: str, *, max_split=None):
        if max_split == 0:
            yield s
            return
        for i in range(len(s)):
            sub = s[i:]
            for delimiter in self._delimiters:
                if not sub.startswith(delimiter):
                    continue
                a = s[:i]
                b = s[i + len(delimiter):]
                yield a
                if max_split is None:
                    yield from self.__split_left(b)
                else:
                    yield from self.__split_left(b, max_split=max_split - 1)
                return
        yield s

    def __split_right(self, s: str, *, max_split=None):
        if max_split == 0:
            yield s
            return
        for i in range(len(s), 0, -1):
            sub = s[:i]
            for delimiter in self._delimiters:
                if not sub.endswith(delimiter):
                    continue
                a = s[i:]
                b = s[:i - len(delimiter)]
                yield a
                if max_split is None:
                    yield from self.__split_left(b)
                else:
                    yield from self.__split_left(b, max_split=max_split - 1)
                return
        yield s

    def _split(self, s: str):
        if self.__from_right:
            return self.__split_right(s, max_split=self.__max_split)
        else:
            return self.__split_left(s, max_split=self.__max_split)

    def _parse(self, s: str):
        return [
            self.__fields[i].parse(item)
            for i, item in enumerate(super()._parse(s))
        ]

    def _set_children_schema(self, val: 'CsvFieldSchema'):
        for field in self.__fields:
            field.schema = val

    def _set_children_name(self, val: str):
        for i, field in enumerate(self.__fields):
            field.name = f"{val}[{i}]"

    @property
    def type_name(self) -> str:
        fields_type_names = ', '.join(
            field.type_name
            for field in self.__fields
        )
        return f"{super().type_name}[{fields_type_names}]"


class TextField(Field):
    """
    Text field
    """

    TYPE = str


class _NumericField(Field):
    COMMA = False

    def __init__(
            self,
            *,
            comma: bool = None,
            **kwargs,
    ):
        """
        :param comma: Allow commas in string
        :param kwargs: See base class
        """

        comma = self._option('comma', comma, type=bool)
        if comma:
            if 'str_replace' not in kwargs:
                kwargs['str_replace'] = {}
            kwargs['str_replace'][','] = ''
        super().__init__(**kwargs)


class IntegerField(_NumericField):
    """
    Integer field
    """

    TYPE = int


class FloatField(_NumericField):
    """
    Float field
    """

    TYPE = float


class DateTimeField(Field):
    """
    Date/time field
    """

    FORMAT = None

    TYPE = time.struct_time

    def __init__(
            self,
            format: str = None,
            **kwargs,
    ):
        super().__init__(**kwargs)
        self.__format = self._option('format', format)

    def _parse(self, s: str):
        return time.strptime(s, self.__format)


class CleanTextField(TextField):
    """
    A text field with a limited character set.
    """

    ALLOWED = None
    WARN_STR = None

    PUNCTUATION_NO_DELIMITER = string.punctuation.replace(',', '').replace(';', '')

    def __init__(
            self,
            allowed: Collection[str] = None,
            *,
            warn_str: Collection[str] = None,
            **kwargs,
    ):
        """
        :param allowed:
            A character set to be allowed in the string.
        :param warn_str:
            A substring set to send a log with `WARNING` level.
            All characters still need to be allowed first.
        :param kwargs: See base classes.
        """

        super().__init__(**kwargs)
        self.__allowed = self._option('allowed', allowed, type=set)
        self.__warn_str = self._option('warn_str', warn_str, nullable=True, type=set)

    def _validate_post(self, s):
        super()._validate_pre(s)
        for c in s:
            if c in self.__allowed:
                continue
            msg = f"invalid char '{c}'({ord(c)}) found"
            if self.raises:
                self._raise(s, msg)
            else:
                self._error(s, msg, unique=True)

        if self.__warn_str is not None:
            for substr in self.__warn_str:
                if substr not in s:
                    continue
                self._warn(s, f"warning str '{substr}' found", unique=True)


class ChoiceField(Field):
    """
    A field with a limited set of choices
    """

    CHOICES = None

    def __init__(
            self,
            choices: Collection = None,
            **kwargs,
    ):
        super().__init__(**kwargs)
        self.__choices = self._option('choices', choices, type=set)

    def _validate_post(self, val):
        super()._validate_post(val)
        if val not in self.__choices:
            self._raise(val, 'invalid choice', self.__choices)


class UrlField(CleanTextField):
    """
    A field with valid url characters
    """

    ALLOWED = string.ascii_letters + string.digits + './:_-'


class BoolField(Field):
    """
    A boolean field
    """

    TYPE = bool
    TRUE = None
    FALSE = None

    def __init__(
            self,
            *,
            true: Collection[str] = None,
            false: Collection[str] = None,
            **kwargs,
    ):
        """
        :param true: A collection of strings to be considered True.
        :param false: A collection of strings to be considered False.
        :param kwargs: See base class.
        """

        super().__init__(**kwargs)
        self.__true = self._option('true', true, type=set)
        self.__false = self._option('false', false, type=set)

    def _parse(self, s: str):
        if s in self.__true:
            return True
        elif s in self.__false:
            return False
        else:
            self._raise(s, 'not true/false')


class CsvFieldSchema(CsvSchema):
    """
    A csv schema with fields
    """

    class ColumnParseError(Exception):
        def __init__(
                self,
                lineno: int,
                column_name: str,
                field_type: str,
                value: str,
        ):
            super().__init__(
                f"Line {lineno}: "
                f"Cannot parse column '{column_name}', "
                f"expected type {field_type}, "
                f"value: '{value}'"
            )

    def __init__(
            self,
            fields: Sequence[Tuple[Union[int, str], Field]],
            **kwargs,
    ):
        """
        Return a dict parsed according to field configuration.
        Only columns specified will be returned.

        :param fields: Field configuration
            fields = (
                (0, IntegerField()),  # the first column is an integer
                ('uuid', TextField()),  # the column named 'uuid' is a text
            )
        :param kwargs: See base classes
            `as_dict` will be set to False
        """

        if 'as_dict' in kwargs:
            logger_module.warning('`as_dict` is always False in `CsvFieldSchema`')
        kwargs['as_dict'] = False
        self.__fields = tuple(fields)
        for _, field in self.__fields:
            field.schema = self

        self.__fields_indexed = None
        self.__current_field = None
        self.__current_field_value = None
        super().__init__(**kwargs)

    def reset(self):
        self.__fields_indexed = None
        self.__current_field = None
        self.__current_field_value = None
        super().reset()

    @returns(list)
    def indexed_fields(self, header: Sequence[str] = None) -> List[Tuple[int, Field]]:
        """
        Find index for columns in the header
        """
        if header is None:
            header = self.header
        for key_or_index, field in self.__fields:
            if isinstance(key_or_index, int):
                index = key_or_index
                try:
                    key = header[index]
                except IndexError:
                    raise self.SetupError(f"index {index} not in header") from None
            else:
                key = key_or_index
                try:
                    index = header.index(key)
                except ValueError:
                    raise self.SetupError(f"'{key}' not in header") from None
            field.name = key
            yield index, field

    def _index_fields(self):
        self.__fields_indexed = self.indexed_fields()

    @property
    def fields(self) -> List[Tuple[int, Field]]:
        return self.__fields_indexed

    def _set_header(self, header: Iterable[str]):
        super()._set_header(header)
        self._index_fields()

    @returns(dict)
    def parse_fields(self, result: Sequence[str]) -> Dict[str, Any]:
        for i, field in self.fields:
            key = self.header[i]
            try:
                value = result[i]
            except IndexError:
                value = None
            try:
                self.__current_field = key
                self.__current_field_value = value
                value = field.parse(value)
            except Exception:
                raise self.ColumnParseError(self.lineno, key, field.type_name, value)
            yield key, value

    @property
    def context(self) -> Dict[str, Any]:
        return {
            'lineno': self.lineno,
            'line': self._line,
            'field': self.__current_field,
            'value': self.__current_field_value,
        }

    def _read_data_line(self):
        result = super()._read_data_line()
        return self.parse_fields(result)
