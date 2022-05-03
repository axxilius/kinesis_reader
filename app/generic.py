import asyncio
import collections.abc
import orjson

import boto3
from logging import Logger
import backoff
from concurrent.futures import ThreadPoolExecutor
from botocore.exceptions import ClientError

import it_pylogger
import settings


class KinesisClient:
    def __init__(
        self,
        aws_key: str,
        aws_secret: str,
        aws_region: str,
        aws_endpoint: str,
        logger: Logger
    ):
        self._transport = boto3.client(
            'kinesis',
            region_name=aws_region,
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret,
            endpoint_url=aws_endpoint,
        )
        self._executor = ThreadPoolExecutor()
        self._logger = logger

    @backoff.on_exception(backoff.expo, ClientError, max_tries=3)
    def _pub(
        self,
        stream_name: str,
        partition_key: str,
        data: collections.abc.Mapping
    ):
        try:
            json_data = orjson.dumps(data)
            self._transport.put_record(
                StreamName=stream_name,
                Data=json_data,
                PartitionKey=partition_key
            )
        except Exception as e:
            self._logger.exception(e)
            raise
        else:
            self._logger.info(dict(
                message='Data has been sent to kinesis',
                stream_name=stream_name,
                partition_key=partition_key,
                keys=list(data.keys()),
            ))

    async def pub(self, stream_name: str, partition_key: str, data: collections.abc.Mapping):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._executor,
            self._pub,
            stream_name,
            partition_key,
            data
        )

    async def describe_stream(self, StreamName: str):
        return self._transport.describe_stream(StreamName=StreamName)

    async def get_shard_iterator(self, **kwargs):
        return self._transport.get_shard_iterator(**kwargs)

    async def get_records(self, **kwargs):
        return self._transport.get_records(**kwargs)


client = KinesisClient(
    aws_key=settings.AWS_KEY,
    aws_secret=settings.AWS_SECRET_KEY,
    aws_region=settings.KINESIS_REGION,
    aws_endpoint=settings.KINESIS_ENDPOINT_URL,
    logger=it_pylogger.logger
)
