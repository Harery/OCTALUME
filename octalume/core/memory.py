"""Long-term memory bank for OCTALUME."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from octalume.utils.logging import get_logger

logger = get_logger(__name__)


class MemoryBank:
    """Persistent memory storage for decisions, progress, and context."""

    def __init__(self, memory_dir: Path | None = None):
        self.memory_dir = memory_dir or Path.cwd() / ".octalume" / "memory"
        self.memory_file = self.memory_dir / "memory.json"
        self._ensure_memory_dir()
        self._memory: dict[str, Any] = self._load_memory()

    def _ensure_memory_dir(self) -> None:
        """Ensure memory directory exists."""
        self.memory_dir.mkdir(parents=True, exist_ok=True)

    def _load_memory(self) -> dict[str, Any]:
        """Load memory from disk."""
        if not self.memory_file.exists():
            return self._create_empty_memory()

        try:
            with open(self.memory_file) as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            logger.error("memory_load_error", error=str(e))
            return self._create_empty_memory()

    def _create_empty_memory(self) -> dict[str, Any]:
        """Create empty memory structure."""
        return {
            "version": "2.0.0",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "memory": {
                "decisions": {},
                "progress": {},
                "blockers": {},
                "notes": {},
                "context": {},
                "traces": [],
            },
            "statistics": {
                "total_entries": 0,
                "decisions": 0,
                "progress": 0,
                "blockers": 0,
                "notes": 0,
            },
        }

    def _save_memory(self) -> None:
        """Save memory to disk."""
        self._memory["updated_at"] = datetime.utcnow().isoformat()

        with open(self.memory_file, "w") as f:
            json.dump(self._memory, f, indent=2)

        logger.debug("memory_saved", entries=self._memory["statistics"]["total_entries"])

    def save(
        self,
        category: str,
        key: str,
        value: Any,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Save a memory entry."""
        if category not in self._memory["memory"]:
            self._memory["memory"][category] = {}

        entry_id = f"{category}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{key[:8]}"

        entry = {
            "id": entry_id,
            "key": key,
            "value": value,
            "metadata": metadata or {},
            "created_at": datetime.utcnow().isoformat(),
        }

        self._memory["memory"][category][key] = entry
        self._memory["statistics"]["total_entries"] += 1

        if category in self._memory["statistics"]:
            self._memory["statistics"][category] += 1

        self._save_memory()

        logger.info("memory_entry_saved", category=category, key=key, entry_id=entry_id)

        return entry_id

    def load(self, category: str, key: str) -> Any | None:
        """Load a memory entry."""
        if category not in self._memory["memory"]:
            return None

        entry = self._memory["memory"][category].get(key)

        if entry:
            logger.debug("memory_entry_loaded", category=category, key=key)
            return entry.get("value")

        return None

    def query(
        self,
        category: str | None = None,
        search_term: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Query memory entries."""
        results = []

        categories = [category] if category else list(self._memory["memory"].keys())

        for cat in categories:
            if cat not in self._memory["memory"]:
                continue

            for key, entry in self._memory["memory"][cat].items():
                if search_term and search_term.lower() not in key.lower():
                    if isinstance(entry.get("value"), str):
                        if search_term.lower() not in entry["value"].lower():
                            continue
                    else:
                        continue

                results.append({
                    "category": cat,
                    "key": key,
                    "entry": entry,
                })

                if len(results) >= limit:
                    return results

        return results

    def delete(self, category: str, key: str) -> bool:
        """Delete a memory entry."""
        if category not in self._memory["memory"]:
            return False

        if key not in self._memory["memory"][category]:
            return False

        del self._memory["memory"][category][key]
        self._memory["statistics"]["total_entries"] -= 1

        if category in self._memory["statistics"]:
            self._memory["statistics"][category] -= 1

        self._save_memory()

        logger.info("memory_entry_deleted", category=category, key=key)

        return True

    def list_categories(self) -> list[str]:
        """List all memory categories."""
        return list(self._memory["memory"].keys())

    def get_statistics(self) -> dict[str, Any]:
        """Get memory statistics."""
        return self._memory["statistics"].copy()

    def clear_category(self, category: str) -> int:
        """Clear all entries in a category."""
        if category not in self._memory["memory"]:
            return 0

        count = len(self._memory["memory"][category])

        self._memory["statistics"]["total_entries"] -= count
        if category in self._memory["statistics"]:
            self._memory["statistics"][category] = 0

        self._memory["memory"][category] = {}

        self._save_memory()

        logger.warning("memory_category_cleared", category=category, entries_removed=count)

        return count

    def add_trace(
        self,
        phase: int,
        action: str,
        artifact_id: str | None = None,
        agent_id: str | None = None,
        duration_ms: float | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Add a trace entry for observability."""
        trace_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "phase": phase,
            "action": action,
            "artifact_id": artifact_id,
            "agent_id": agent_id,
            "duration_ms": duration_ms,
            "metadata": metadata or {},
        }

        self._memory["memory"]["traces"].append(trace_entry)

        if len(self._memory["memory"]["traces"]) > 10000:
            self._memory["memory"]["traces"] = self._memory["memory"]["traces"][-5000:]

        self._save_memory()

        return trace_entry["timestamp"]

    def get_traces(
        self,
        phase: int | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Get trace entries."""
        traces = self._memory["memory"]["traces"]

        if phase is not None:
            traces = [t for t in traces if t["phase"] == phase]

        return traces[-limit:]

    def compress_context(self, max_entries: int = 50) -> int:
        """Compress old context entries to save space."""
        if "context" not in self._memory["memory"]:
            return 0

        context = self._memory["memory"]["context"]

        if len(context) <= max_entries:
            return 0

        sorted_keys = sorted(
            context.keys(),
            key=lambda k: context[k].get("created_at", ""),
        )

        keys_to_remove = sorted_keys[:-max_entries]

        for key in keys_to_remove:
            del context[key]

        removed = len(keys_to_remove)
        self._memory["statistics"]["total_entries"] -= removed
        self._memory["statistics"].setdefault("context", 0)

        self._save_memory()

        logger.info("memory_context_compressed", entries_removed=removed)

        return removed
