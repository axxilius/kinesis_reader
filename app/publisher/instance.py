import collections.abc

import settings
from app.generic import client


async def publish(data: collections.abc.Mapping):
    await client.pub(
        stream_name=settings.KINESIS_STREAM_NAME,
        partition_key=settings.KINESIS_SEQUENCE_KEY,
        data=data
    )
