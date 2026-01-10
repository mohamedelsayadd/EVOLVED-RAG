from redis.asyncio import Redis, ConnectionPool
import time
import asyncio
from typing import Optional

class SlidingWindowLogLimiter:
    def __init__(
        self,
        limit: int,
        window_seconds: int,
        redis_url: str = "redis://localhost:6379",
        prefix: str = "rate_limit"
    ):  
        self.redis_url = redis_url
        self.pool = ConnectionPool.from_url(redis_url)
        self.redis: Redis = Redis(connection_pool=self.pool)
        self.limit = limit
        self.window = window_seconds
        self.prefix = prefix
    
    async def connect(self):
        self.redis = await Redis.from_url(url=self.redis_url, decode_responses = True)
    
    def _key(self, identifier: str) -> str:
        return f"{self.prefix}:{identifier}"
    
    async def is_allowed(self, identifier: str) -> bool:
        
        key = self._key(identifier=identifier)
        now = time.time()
        window_start = now - self.window
        
        pipeline = self.redis.pipeline()
        pipeline.zremrangebyscore(key, 0, window_start)
        pipeline.zadd(key, {now: now}) 
 
        pipeline.zcard(key)
        pipeline.expire(key, self.window + 1)
        
        results = await pipeline.execute()
        
        request_count = results[2]
        return request_count <= self.limit