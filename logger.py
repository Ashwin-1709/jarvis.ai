import logging
import sys
import inspect


def log_with_context(level, message):
    """
    Logs a message to stderr with the current function name and line number.

    Args:
    level: The logging level (e.g., logging.DEBUG, logging.INFO).
    message: The message to log.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    # Create a custom formatter to include function context
    formatter = logging.Formatter(
        f"%(asctime)s - %(levelname)s - {inspect.stack()[1][3]}:{inspect.stack()[1][2]} - %(message)s"
    )

    # Create a handler to log to stderr
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    logger.log(level, message)
