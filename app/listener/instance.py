import asyncio
import settings
from app.generic import client


async def listener(delay=10):
    descr = await client.describe_stream(settings.KINESIS_STREAM_NAME)
    stream = descr['StreamDescription']
    shard_iterator = (await client.get_shard_iterator(
        StreamName=stream.get('StreamName'),
        ShardId=stream.get('Shards')[0].get('ShardId'),
        # ShardIteratorType="LATEST",
        ShardIteratorType="TRIM_HORIZON",
        # StartingSequenceNumber=None
    ))['ShardIterator']

    while shard_iterator is not None:
        result = await client.get_records(ShardIterator=shard_iterator)
        print(result)
        shard_iterator = result["NextShardIterator"]
        await asyncio.sleep(delay)
