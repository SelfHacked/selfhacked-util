import boto3
import tempfile
from botocore.response import StreamingBody
from io import BytesIO
from typing import Iterator, BinaryIO

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

    def __eq__(self, other):
        if not isinstance(other, S3File):
            return False
        if not self.bucket == other.bucket:
            return False
        if not self.key == other.key:
            return False
        return True

    def get_obj(self):
        return self.s3.Object(self.__bucket, self.__key)

    def get_body(self) -> StreamingBody:
        return self.get_obj().get()['Body']

    def read_all(self) -> bytes:
        body = self.get_body()
        try:
            return body.read()
        finally:
            body.close()

    def as_iter(self, *, lines=False) -> Iterator[bytes]:
        body = self.get_body()
        try:
            if lines:
                yield from body.iter_lines()
            else:
                yield from body.iter_chunks()
        finally:
            body.close()

    def as_stream(self, *, lines=False) -> Stream[bytes]:
        return IterStream(self.as_iter(lines=lines))

    def upload_from(self, filename: str):
        self.get_obj().upload_file(filename)

    def upload(self, file: BinaryIO):
        self.get_obj().upload_fileobj(file)

    def copy_to(
            self,
            other: 'S3File' = None,
            *,
            bucket: str = None,
            key: str = None,
            in_memory=True,
    ):
        if other is None:
            if bucket is None:
                # copy to same bucket
                bucket = self.bucket
            if key is None:
                # keep file name
                key = self.key
            other = S3File(bucket, key)
        if self == other:
            raise OSError('Cannot copy to same s3 file')

        if in_memory:
            other.upload(BytesIO(self.read_all()))
        else:
            with tempfile.TemporaryFile() as f:
                for chunk in self.as_iter(lines=False):
                    f.write(chunk)
                f.seek(0, 0)
                other.upload(f)


def upload_cmd():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('bucket')
    parser.add_argument('key')
    args = parser.parse_args()
    S3File(args.bucket, args.key).upload_from(args.file)


def download_cmd():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('bucket')
    parser.add_argument('key')
    parser.add_argument('file')
    args = parser.parse_args()
    with open(args.file, 'wb') as f:
        for chunk in S3File(args.bucket, args.key).as_iter(lines=False):
            f.write(chunk)


def get_cmd():
    """
    Stream to stdout
    """
    import sys
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('bucket')
    parser.add_argument('key')
    args = parser.parse_args()
    for chunk in S3File(args.bucket, args.key).as_iter(lines=False):
        sys.stdout.buffer.write(chunk)


def copy_cmd():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('from-bucket')
    parser.add_argument('from-key')
    parser.add_argument('to-bucket')
    parser.add_argument('to-key')
    parser.add_argument('--in-memory', action='store_true')
    args = parser.parse_args()

    S3File(
        args.from_bucket,
        args.from_key,
    ).copy_to(
        bucket=args.to_bucket,
        key=args.to_key,
        in_memory=args.in_memory,
    )
