"""
缓存管理

提供Redis缓存支持，包括键值缓存、会话存储等。
"""

import json
import pickle
from typing import Any, Optional, Union
from datetime import timedelta

import redis.asyncio as redis
from redis.asyncio import Redis

from .config import settings

# Redis连接池
redis_pool: Optional[Redis] = None


async def get_redis() -> Redis:
    """获取Redis连接"""
    global redis_pool
    if redis_pool is None:
        redis_pool = redis.from_url(
            settings.redis.url,
            encoding="utf-8",
            decode_responses=settings.redis.decode_responses,
            max_connections=settings.redis.pool_size,
        )
    return redis_pool


async def close_redis() -> None:
    """关闭Redis连接"""
    global redis_pool
    if redis_pool:
        await redis_pool.close()
        redis_pool = None


class CacheManager:
    """缓存管理器"""
    
    def __init__(self):
        self.redis: Optional[Redis] = None
    
    async def get_connection(self) -> Redis:
        """获取Redis连接"""
        if self.redis is None:
            self.redis = await get_redis()
        return self.redis
    
    async def set(
        self,
        key: str,
        value: Any,
        expire: Optional[Union[int, timedelta]] = None,
        serialize: bool = True,
    ) -> bool:
        """设置缓存"""
        redis_client = await self.get_connection()
        
        if serialize:
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            else:
                value = str(value)
        
        if expire:
            if isinstance(expire, timedelta):
                expire = int(expire.total_seconds())
            return await redis_client.setex(key, expire, value)
        else:
            return await redis_client.set(key, value)
    
    async def get(
        self, key: str, default: Any = None, deserialize: bool = True
    ) -> Any:
        """获取缓存"""
        redis_client = await self.get_connection()
        value = await redis_client.get(key)
        
        if value is None:
            return default
        
        if deserialize:
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
        
        return value
    
    async def delete(self, key: str) -> bool:
        """删除缓存"""
        redis_client = await self.get_connection()
        return bool(await redis_client.delete(key))
    
    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        redis_client = await self.get_connection()
        return bool(await redis_client.exists(key))
    
    async def expire(self, key: str, seconds: int) -> bool:
        """设置过期时间"""
        redis_client = await self.get_connection()
        return bool(await redis_client.expire(key, seconds))
    
    async def ttl(self, key: str) -> int:
        """获取剩余生存时间"""
        redis_client = await self.get_connection()
        return await redis_client.ttl(key)
    
    async def incr(self, key: str, amount: int = 1) -> int:
        """递增计数器"""
        redis_client = await self.get_connection()
        return await redis_client.incr(key, amount)
    
    async def decr(self, key: str, amount: int = 1) -> int:
        """递减计数器"""
        redis_client = await self.get_connection()
        return await redis_client.decr(key, amount)
    
    async def hset(self, name: str, key: str, value: Any) -> bool:
        """设置哈希字段"""
        redis_client = await self.get_connection()
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        return bool(await redis_client.hset(name, key, value))
    
    async def hget(self, name: str, key: str, default: Any = None) -> Any:
        """获取哈希字段"""
        redis_client = await self.get_connection()
        value = await redis_client.hget(name, key)
        
        if value is None:
            return default
        
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    
    async def hgetall(self, name: str) -> dict:
        """获取所有哈希字段"""
        redis_client = await self.get_connection()
        data = await redis_client.hgetall(name)
        result = {}
        
        for key, value in data.items():
            try:
                result[key] = json.loads(value)
            except (json.JSONDecodeError, TypeError):
                result[key] = value
        
        return result
    
    async def sadd(self, name: str, *values: Any) -> int:
        """添加集合元素"""
        redis_client = await self.get_connection()
        serialized_values = []
        for value in values:
            if isinstance(value, (dict, list)):
                serialized_values.append(json.dumps(value, ensure_ascii=False))
            else:
                serialized_values.append(str(value))
        return await redis_client.sadd(name, *serialized_values)
    
    async def smembers(self, name: str) -> set:
        """获取集合所有元素"""
        redis_client = await self.get_connection()
        members = await redis_client.smembers(name)
        result = set()
        
        for member in members:
            try:
                result.add(json.loads(member))
            except (json.JSONDecodeError, TypeError):
                result.add(member)
        
        return result


# 全局缓存管理器实例
cache = CacheManager()


# 缓存装饰器
def cached(expire: Optional[Union[int, timedelta]] = None, key_prefix: str = ""):
    """缓存装饰器"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # 尝试从缓存获取
            cached_result = await cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # 执行函数
            result = await func(*args, **kwargs)
            
            # 存储到缓存
            await cache.set(cache_key, result, expire=expire)
            
            return result
        
        return wrapper
    return decorator 