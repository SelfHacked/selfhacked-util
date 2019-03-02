from typing import Any, Collection

from . import _BaseOneToOneFunction


class getitem(_BaseOneToOneFunction[Collection, Any]):
    def __init__(self, index):
        self.__index = index

    def _call(self, item):
        return item[self.__index]
