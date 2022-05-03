from envparse import env

env.read_envfile()

AWS_KEY = env('AWS_KEY', None)
AWS_SECRET_KEY = env('AWS_SECRET_KEY', None)

REDIS_DSN = env('REDIS_DSN', 'redis://localhost:6379/0')
KINESIS_ENDPOINT_URL = env('KINESIS_ENDPOINT_URL', None)
KINESIS_REGION = env('KINESIS_REGION', 'eu-central-1')
KINESIS_WORKER_SLEEP_DELAY_SECONDS = env(
    'KINESIS_WORKER_SLEEP_DELAY_SECONDS', 10, cast=int
)

KINESIS_STREAM_NAME = env('KINESIS_STREAM_NAME')
KINESIS_SEQUENCE_KEY = env('KINESIS_SEQUENCE_KEY')
KINESIS_SHARD_OPERATOR_TYPE = env(
    'KINESIS_SHARD_OPERATOR_TYPE', 'AT_SEQUENCE_NUMBER'
)
