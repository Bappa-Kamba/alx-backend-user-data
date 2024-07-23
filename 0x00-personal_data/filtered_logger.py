#!/usr/bin/env python3
""" Filter Logger Module """
import logging
import re
from typing import List, Tuple

PII_FIELDS: Tuple[str, ...] = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """
        Function to filter and redact records.

        Args:
            fields: fields to redact
            redaction: redaction string
            message: message that contains fields to redact
            separator: string separating the fields

        Returns:
            redacted string
    """
    return re.sub(
        rf'({"|".join(f"{field}=[^ {separator}]+" for field in fields)})',
        lambda m: f"{m.group(0).split('=')[0]}={redaction}",
        message
    )


def get_logger() -> logging.Logger:
    """
        Create and configure a logger.

        Returns:
            logging.Logger: Configured logger named 'user_data'
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.addHandler(stream_handler)

    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Redact fields in the log record """
        original_message = super().format(record)
        return filter_datum(
            self.fields,
            self.REDACTION,
            original_message,
            self.SEPARATOR,
        )
