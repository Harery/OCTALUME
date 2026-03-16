"""Message bus for agent communication."""

import asyncio
from collections import defaultdict
from datetime import datetime
from typing import Any
from uuid import uuid4

from octalume.utils.logging import get_logger

logger = get_logger(__name__)


class MessageBus:
    """Async message bus for agent-to-agent communication."""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[Any]] = defaultdict(list)
        self._queues: dict[str, asyncio.Queue[Any]] = {}
        self._message_log: list[dict[str, Any]] = []
        self._max_log_size = 10000

    async def subscribe(
        self,
        agent_id: str,
        handler: Any | None = None,
    ) -> asyncio.Queue[Any]:
        """Subscribe an agent to receive messages."""
        if agent_id not in self._queues:
            self._queues[agent_id] = asyncio.Queue()

        if handler and handler not in self._subscribers[agent_id]:
            self._subscribers[agent_id].append(handler)

        logger.info("message_bus_subscribe", agent_id=agent_id)

        return self._queues[agent_id]

    async def unsubscribe(
        self,
        agent_id: str,
        handler: Any | None = None,
    ) -> None:
        """Unsubscribe an agent from messages."""
        if handler and handler in self._subscribers[agent_id]:
            self._subscribers[agent_id].remove(handler)

        if not handler:
            self._subscribers[agent_id] = []
            if agent_id in self._queues:
                del self._queues[agent_id]

        logger.info("message_bus_unsubscribe", agent_id=agent_id)

    async def publish(
        self,
        recipient: str,
        message: dict[str, Any],
    ) -> bool:
        """Publish a message to a recipient's queue."""
        if recipient not in self._queues:
            logger.warning(
                "message_bus_no_queue",
                recipient=recipient,
            )
            return False

        await self._queues[recipient].put(message)

        self._log_message(message)

        return True

    async def receive(
        self,
        agent_id: str,
        timeout: float = 1.0,
    ) -> dict[str, Any] | None:
        """Receive a message for an agent."""
        if agent_id not in self._queues:
            return None

        try:
            message = await asyncio.wait_for(
                self._queues[agent_id].get(),
                timeout=timeout,
            )
            return message
        except TimeoutError:
            return None

    async def get_subscribers(self) -> list[str]:
        """Get list of all subscriber agent IDs."""
        return list(self._queues.keys())

    async def get_queue_size(self, agent_id: str) -> int:
        """Get the number of pending messages for an agent."""
        if agent_id not in self._queues:
            return 0
        return self._queues[agent_id].qsize()

    def _log_message(self, message: dict[str, Any]) -> None:
        """Log a message for audit/history."""
        log_entry = {
            "id": message.get("id", f"log-{uuid4().hex[:8]}"),
            "timestamp": datetime.utcnow().isoformat(),
            "sender": message.get("sender"),
            "recipient": message.get("recipient"),
            "type": message.get("type"),
        }

        self._message_log.append(log_entry)

        if len(self._message_log) > self._max_log_size:
            self._message_log = self._message_log[-self._max_log_size // 2 :]

    def get_message_log(
        self,
        agent_id: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Get message log, optionally filtered by agent."""
        logs = self._message_log

        if agent_id:
            logs = [
                log
                for log in logs
                if log.get("sender") == agent_id or log.get("recipient") == agent_id
            ]

        return logs[-limit:]

    def get_stats(self) -> dict[str, Any]:
        """Get message bus statistics."""
        return {
            "total_subscribers": len(self._queues),
            "total_messages_logged": len(self._message_log),
            "pending_messages": sum(q.qsize() for q in self._queues.values()),
            "subscribers": {
                agent_id: {
                    "pending": queue.qsize(),
                    "handlers": len(self._subscribers.get(agent_id, [])),
                }
                for agent_id, queue in self._queues.items()
            },
        }

    async def clear_queue(self, agent_id: str) -> int:
        """Clear all pending messages for an agent."""
        if agent_id not in self._queues:
            return 0

        count = self._queues[agent_id].qsize()

        while not self._queues[agent_id].empty():
            try:
                self._queues[agent_id].get_nowait()
            except asyncio.QueueEmpty:
                break

        return count

    async def broadcast_to_all(
        self,
        message: dict[str, Any],
        exclude: list[str] | None = None,
    ) -> list[str]:
        """Broadcast a message to all subscribers."""
        exclude = exclude or []
        delivered = []

        for agent_id in self._queues:
            if agent_id not in exclude and agent_id != message.get("sender"):
                success = await self.publish(agent_id, message)
                if success:
                    delivered.append(agent_id)

        return delivered
