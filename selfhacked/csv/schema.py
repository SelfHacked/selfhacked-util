import csv
from logging import Logger
from typing import Iterable, Any, Iterator, Optional, List, Union, Dict, Sequence, Tuple

from selfhacked.util.func import returns


class Schema(object):
    """
    Abstract schema.
    Subclasses should call super().__init__() at the end of the init function because it will call reset()
    """

    class SetupError(Exception):
        pass

    def __init__(
            self,
            *,
            logger: Logger = None,
    ):
        self.__logger = logger

        self.__lineno = None
        self.__line = None
        self.reset()

    @property
    def logger(self) -> Logger:
        return self.__logger

    @property
    def lineno(self) -> int:
        return self.__lineno

    @property
    def _line(self) -> str:
        return self.__line

    def reset(self) -> None:
        self.__lineno = -1
        self.__line = None

    def read_line(self, line: str) -> Optional:
        """
        Read one line and return the result if it's a data line
        """
        self.__line = line
        self.__lineno += 1
        return self._read_line()

    def read_lines(self, lines: Iterable[str]) -> Iterator:
        """
        Read multiple lines and return the results
        """
        for line in lines:
            result = self.read_line(line)
            if result is None:
                continue
            yield result

    def read_file(self, lines: Iterable[str]) -> Iterator:
        """
        Read a new file
        """
        self.reset()
        yield from self.read_lines(lines)

    def _read_line(self) -> Optional:
        if self._is_header_line:
            return self._read_header_line()
        else:
            return self._read_data_line()

    @property
    def _is_header_line(self) -> bool:
        raise NotImplementedError  # pragma: no cover

    def _read_header_line(self) -> None:
        raise NotImplementedError  # pragma: no cover

    @property
    def _is_data_line(self) -> bool:
        return not self._is_header_line  # pragma: no cover

    def _read_data_line(self) -> Any:
        raise NotImplementedError  # pragma: no cover


class CsvSchema(Schema):
    """
    A text csv schema
    """

    def __init__(
            self,
            *,
            delimiter=',',
            header: Union[Sequence[str], bool] = True,
            replace_header: Optional[Dict[str, str]] = None,
            strip_columns=True,
            as_dict=False,
            **kwargs,
    ):
        """
        :param delimiter: default ','
        :param header:
            If True (default), read one line as header;
            If False, do not read line as header;
            Otherwise (must be sequence of str), use as header.
        :param replace_header:
            Replace column names in the header - invalid if `header` is False.
        :param strip_columns: default True
        :param as_dict:
            If True, return dict with headers as keys - invalid if `header` is False;
            If False (default), return list.
        :param kwargs: See base class.
        """

        self.__delimiter = delimiter
        self.__header = header
        self.__replace_header = replace_header
        self.__strip_columns = strip_columns
        self.__as_dict = as_dict

        if not self.has_header:
            if replace_header is not None:
                raise self.SetupError('`replace_header` is set, but `header` is False')
            if as_dict:
                raise self.SetupError('`as_dict` is True, but `header` is False')

        self.__header_actual = None
        super().__init__(**kwargs)

    @property
    def has_header(self) -> bool:
        return bool(self.__header)

    @property
    def _reads_header(self) -> bool:
        return self.__header is True

    @returns(tuple)
    def replace_header(self, header: Iterable[str]) -> Tuple[str, ...]:
        if self.__replace_header is None:
            yield from header
            return
        for item in header:
            if item in self.__replace_header:
                item = self.__replace_header[item]
            yield item

    def _set_header(self, header: Iterable[str]):
        self.__header_actual = self.replace_header(header)

    def _reset_header(self):
        self.__header_actual = None
        if isinstance(self.__header, bool):
            return
        self._set_header(self.__header)

    @property
    def header(self) -> Tuple[str, ...]:
        return self.__header_actual

    def reset(self):
        self._reset_header()
        super().reset()

    @property
    def _is_header_line(self):
        return self._reads_header and self.lineno == 0

    def split(self, line: str = None) -> List[str]:
        if line is None:
            line = self._line
        # result = line.split(self.__delimiter)
        result = next(csv.reader([line], delimiter=self.__delimiter))
        if self.__strip_columns:
            result = [
                item.strip()
                for item in result
            ]
        return result

    def _read_header_line(self):
        self._set_header(self.split())

    @returns(dict)
    def as_dict(self, items: Sequence) -> Dict[str, Any]:
        for i, key in enumerate(self.header):
            try:
                value = items[i]
            except IndexError:
                value = None
            yield key, value

    def _read_data_line(self):
        items = self.split()
        if self.__as_dict:
            items = self.as_dict(items)
        return items
