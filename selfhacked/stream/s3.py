import boto3
from botocore.response import StreamingBody

from . import Stream


class S3Stream(Stream):
    s3 = boto3.resource('s3')

    def __init__(self, bucket, key, lines=False):
        self.__bucket = bucket
        self.__key = key
        self.__lines = lines
        self.__stream: StreamingBody = None

    def _open(self):
        obj = self.s3.Object(self.__bucket, self.__key)
        self.__stream = obj.get()['Body']

    def _close(self):
        self.__stream.close()

    def _iter(self):
        if self.__lines:
            yield from self.__stream.iter_lines()
        else:
            yield from self.__stream.iter_chunks()
