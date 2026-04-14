"""Logging helpers for workflow scripts."""

import logging


def get_logger(name: str = "workflow1") -> logging.Logger:
    """Return a package logger with a simple stream handler."""

    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
