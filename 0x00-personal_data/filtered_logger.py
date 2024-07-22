#!/usr/bin/env python3
""" Filter Logger Module """
import re


def filter_datum(
        fields: list,
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
