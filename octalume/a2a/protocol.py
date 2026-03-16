"""Agent-to-Agent protocol implementation."""

from datetime import datetime
from typing import Any
from uuid import uuid4

from octalume.utils.logging import get_logger

logger = get_logger(__name__)


class A2AProtocol:
    """Agent-to-Agent communication protocol."""

    def __init__(self, message_bus: Any):
        self.message_bus = message_bus
        self._message_handlers: dict[str, Any] = {}
        self._pending_responses: dict[str, Any] = {}

    async def send_message(
        self,
        sender: str,
        recipient: str,
        message_type: str,
        payload: dict[str, Any],
        correlation_id: str | None = None,
        timeout_seconds: int = 300,
    ) -> str:
        """Send a message from one agent to another."""
        message_id = f"msg-{uuid4().hex[:12]}"

        message = {
            "id": message_id,
            "sender": sender,
            "recipient": recipient,
            "type": message_type,
            "payload": payload,
            "correlation_id": correlation_id,
            "timestamp": datetime.utcnow().isoformat(),
            "timeout_seconds": timeout_seconds,
            "status": "sent",
        }

        await self.message_bus.publish(recipient, message)

        logger.info(
            "a2a_message_sent",
            message_id=message_id,
            sender=sender,
            recipient=recipient,
            type=message_type,
        )

        return message_id

    async def send_request(
        self,
        sender: str,
        recipient: str,
        request_type: str,
        payload: dict[str, Any],
        timeout_seconds: int = 300,
    ) -> str:
        """Send a request and wait for response."""
        correlation_id = f"req-{uuid4().hex[:12]}"

        message_id = await self.send_message(
            sender=sender,
            recipient=recipient,
            message_type=request_type,
            payload=payload,
            correlation_id=correlation_id,
            timeout_seconds=timeout_seconds,
        )

        self._pending_responses[correlation_id] = {
            "message_id": message_id,
            "sent_at": datetime.utcnow(),
            "timeout_seconds": timeout_seconds,
        }

        return correlation_id

    async def send_response(
        self,
        sender: str,
        recipient: str,
        correlation_id: str,
        payload: dict[str, Any],
        success: bool = True,
    ) -> str:
        """Send a response to a previous request."""
        return await self.send_message(
            sender=sender,
            recipient=recipient,
            message_type="response",
            payload={
                "success": success,
                "data": payload,
            },
            correlation_id=correlation_id,
        )

    async def broadcast(
        self,
        sender: str,
        message_type: str,
        payload: dict[str, Any],
        recipients: list[str] | None = None,
    ) -> list[str]:
        """Broadcast a message to multiple recipients."""
        if recipients is None:
            recipients = await self.message_bus.get_subscribers()

        message_ids = []
        for recipient in recipients:
            if recipient != sender:
                message_id = await self.send_message(
                    sender=sender,
                    recipient=recipient,
                    message_type=message_type,
                    payload=payload,
                )
                message_ids.append(message_id)

        return message_ids

    def register_handler(
        self,
        agent_id: str,
        message_type: str,
        handler: Any,
    ) -> None:
        """Register a handler for a specific message type."""
        key = f"{agent_id}:{message_type}"
        self._message_handlers[key] = handler

        logger.info(
            "a2a_handler_registered",
            agent_id=agent_id,
            message_type=message_type,
        )

    async def process_message(
        self,
        recipient: str,
        message: dict[str, Any],
    ) -> Any:
        """Process an incoming message."""
        message_type = message.get("type", "unknown")
        handler_key = f"{recipient}:{message_type}"
        wildcard_key = f"{recipient}:*"

        handler = self._message_handlers.get(handler_key) or self._message_handlers.get(
            wildcard_key
        )

        if handler:
            result = await handler(message)

            if message.get("correlation_id") and message.get("type") != "response":
                await self.send_response(
                    sender=recipient,
                    recipient=message["sender"],
                    correlation_id=message["correlation_id"],
                    payload=result if isinstance(result, dict) else {"result": result},
                )

            return result

        logger.warning(
            "a2a_no_handler",
            recipient=recipient,
            message_type=message_type,
        )

        return None

    def get_pending_requests(self) -> list[dict[str, Any]]:
        """Get all pending requests awaiting response."""
        pending = []
        now = datetime.utcnow()

        for correlation_id, request in self._pending_responses.items():
            elapsed = (now - request["sent_at"]).total_seconds()
            pending.append(
                {
                    "correlation_id": correlation_id,
                    "message_id": request["message_id"],
                    "elapsed_seconds": elapsed,
                    "timeout_seconds": request["timeout_seconds"],
                    "expired": elapsed > request["timeout_seconds"],
                }
            )

        return pending

    def clear_expired_requests(self) -> int:
        """Clear expired pending requests."""
        now = datetime.utcnow()
        expired = []

        for correlation_id, request in self._pending_responses.items():
            elapsed = (now - request["sent_at"]).total_seconds()
            if elapsed > request["timeout_seconds"]:
                expired.append(correlation_id)

        for correlation_id in expired:
            del self._pending_responses[correlation_id]

        if expired:
            logger.warning(
                "a2a_requests_expired",
                count=len(expired),
                correlation_ids=expired,
            )

        return len(expired)
