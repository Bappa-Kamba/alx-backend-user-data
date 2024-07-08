# 1/usr/bin/env python3
""" Filter Logger Module """
import re


def filter_datum(fields: str, redaction: str, message: str, separator: str):
    """
        Filter a message based on a set of fields and a redaction string

        Args:

            fields (str): A comma separated list of fields to filter on
            redaction (str): A string to replace the filtered fields with
            message (str): The message to filter
            separator (str): The separator to use when splitting the message into fields

        Returns:
            str: The filtered message
    """
    pattern = re.compile(
        rf'({"|".join(f"{field}=[^ {separator}]+" for field in fields)})')
    return pattern.sub(lambda m: f"{m.group(0).split('=')[0]}={redaction}", message)
