# 1/usr/bin/env python3
""" Filter Logger Module """
import logging
import re


def filter_datum(fields: str, redaction: str, message: str, separator: str) -> str:
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
    return pattern.sub(lambda m: f" {m.group(0).split('=')[0]}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
            Format a log record

            Args:
                record (logging.LogRecord): The log record to format

            Returns:
                str: The formatted log record
        """
        original_message = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, original_message,
            self.SEPARATOR
        )
    

message = "name=Bob;email=bob@dylan.com;ssn=000-123-0000;password=bobby2019;"
log_record = logging.LogRecord(
    "my_logger", logging.INFO, None, None, message, None, None)
formatter = RedactingFormatter(fields=("email", "ssn", "password"))
print(formatter.format(log_record))
