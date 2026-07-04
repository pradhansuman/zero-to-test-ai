"""Structured logging utilities."""
import logging
import json
from datetime import datetime
from typing import Any, Optional, Dict


class StructuredLogger:
    """Structured logger with context support."""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        # Only add handler once per logger (prevent duplicates)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def info(self, message: str, **context: Any):
        """Log info level with context."""
        self._log(logging.INFO, message, context)

    def warning(self, message: str, **context: Any):
        """Log warning level with context."""
        self._log(logging.WARNING, message, context)

    def error(self, message: str, **context: Any):
        """Log error level with context."""
        self._log(logging.ERROR, message, context)

    def debug(self, message: str, **context: Any):
        """Log debug level with context."""
        self._log(logging.DEBUG, message, context)

    def _log(self, level: int, message: str, context: Dict[str, Any]):
        """Internal log with context."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            "context": context
        }
        self.logger.log(level, json.dumps(log_entry))


def get_logger(name: str) -> StructuredLogger:
    """Get or create a structured logger."""
    return StructuredLogger(name)
