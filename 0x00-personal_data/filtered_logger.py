#!/usr/bin/env python3
""" Filter Logger Module """
import re


def filter_datum(fields, redaction, message, separator):
    pattern = re.compile(
        rf'({"|".join(f"{field}=[^ {separator}]+" for field in fields)})')
    return pattern.sub(
        lambda m: f"{m.group(0).split('=')[0]}={redaction}", message
    )
