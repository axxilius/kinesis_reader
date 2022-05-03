import asyncio
from app.publisher.instance import publish

data = {
    'a': 12
}

asyncio.run(publish(data))
