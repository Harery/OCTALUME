"""Redis caching layer for OCTALUME."""

import json
from typing import Any

import redis.asyncio as aioredis

from octalume.utils.config import settings
from octalume.utils.logging import get_logger

logger = get_logger(__name__)


class CacheManager:
    """Redis-based caching for state and sessions."""

    def __init__(self, redis_url: str | None = None):
        self.redis_url = redis_url or settings.redis_url
        self._redis: aioredis.Redis | None = None
        self._prefix = "octalume:"
        self._default_ttl = 3600

    async def connect(self) -> None:
        if self._redis is None:
            self._redis = await aioredis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True,
            )
            logger.info("redis_connected", url=self.redis_url)

    async def disconnect(self) -> None:
        if self._redis:
            await self._redis.close()
            self._redis = None
            logger.info("redis_disconnected")

    @property
    def redis(self) -> aioredis.Redis:
        if self._redis is None:
            raise RuntimeError("Redis not connected. Call connect() first.")
        return self._redis

    def _key(self, *parts: str) -> str:
        return f"{self._prefix}{':'.join(parts)}"

    async def get(self, category: str, key: str) -> Any | None:
        full_key = self._key(category, key)
        value = await self.redis.get(full_key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None

    async def set(
        self,
        category: str,
        key: str,
        value: Any,
        ttl: int | None = None,
    ) -> bool:
        full_key = self._key(category, key)
        ttl = ttl or self._default_ttl

        if isinstance(value, (dict, list)):
            value = json.dumps(value)

        result = await self.redis.setex(full_key, ttl, value)
        return bool(result)

    async def delete(self, category: str, key: str) -> bool:
        full_key = self._key(category, key)
        result = await self.redis.delete(full_key)
        return result > 0

    async def exists(self, category: str, key: str) -> bool:
        full_key = self._key(category, key)
        return bool(await self.redis.exists(full_key))

    async def get_project_state(self, project_id: str) -> dict | None:
        return await self.get("project_state", project_id)

    async def set_project_state(
        self,
        project_id: str,
        state: dict,
        ttl: int = 300,
    ) -> bool:
        return await self.set("project_state", project_id, state, ttl)

    async def invalidate_project_state(self, project_id: str) -> bool:
        return await self.delete("project_state", project_id)

    async def get_session(self, session_id: str) -> dict | None:
        return await self.get("session", session_id)

    async def set_session(
        self,
        session_id: str,
        data: dict,
        ttl: int = 86400,
    ) -> bool:
        return await self.set("session", session_id, data, ttl)

    async def delete_session(self, session_id: str) -> bool:
        return await self.delete("session", session_id)

    async def acquire_lock(
        self,
        resource: str,
        holder: str,
        ttl: int = 30,
    ) -> bool:
        lock_key = self._key("lock", resource)
        return bool(await self.redis.set(lock_key, holder, ex=ttl, nx=True))

    async def release_lock(self, resource: str, holder: str) -> bool:
        lock_key = self._key("lock", resource)
        current = await self.redis.get(lock_key)
        if current == holder:
            await self.redis.delete(lock_key)
            return True
        return False

    async def get_metrics(self) -> dict[str, Any]:
        info = await self.redis.info()
        return {
            "connected_clients": info.get("connected_clients", 0),
            "used_memory_human": info.get("used_memory_human", "0B"),
            "total_commands_processed": info.get("total_commands_processed", 0),
            "keyspace_hits": info.get("keyspace_hits", 0),
            "keyspace_misses": info.get("keyspace_misses", 0),
        }


cache = CacheManager()
