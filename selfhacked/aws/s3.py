import boto3
from botocore.response import StreamingBody
from typing import Iterator

from selfhacked.iterator.stream import Stream, IterStream


class S3File(object):
    s3 = boto3.resource('s3')

    def __init__(self, bucket: str, key: str):
        self.__bucket = bucket
        self.__key = key

    @property
    def bucket(self) -> str:
        return self.__bucket

    @property
    def key(self) -> str:
        return self.__key

    def get(self) -> StreamingBody:
        obj = self.s3.Object(self.__bucket, self.__key)
        return obj.get()['Body']

    def read_all(self) -> bytes:
        body = self.get()
        try:
            return body.read()
        finally:
            body.close()

    def as_iter(self, *, lines=False) -> Iterator[bytes]:
        body = self.get()
        try:
            if lines:
                yield from body.iter_lines()
            else:
                yield from body.iter_chunks()
        finally:
            body.close()

    def as_stream(self, *, lines=False) -> Stream[bytes]:
        return IterStream(self.as_iter(lines=lines))
