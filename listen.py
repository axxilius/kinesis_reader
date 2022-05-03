import asyncio
from app.listener.instance import listener

asyncio.run(listener(delay=10))
