#!/usr/bin/env python3
"""Unneeded really really long doc"""
from typing import List
import os
import re
import logging
import mysql.connector
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    Some random doc
    """
    for fieldname in fields:
        message = re.sub(f'{fieldname}=.+?{separator}',
                         f"{fieldname}={redaction}{separator}",
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializes a redacting formatter"""
        self.fields = list(fields)
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Format method that redacts sensitive information"""
        return filter_datum(self.fields,
                            self.REDACTION,
                            super().format(record),
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    ------------------
    METHOD: get_logger
    ------------------
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))

    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    --------------
    METHOD: get_db
    --------------
    Description:
        Takes no arguments, but returns
        a connection to the database.
    """
    from os import environ as env

    usr = os.env['PERSONAL_DATA_DB_USERNAME']
    pwd = os.env['PERSONAL_DATA_DB_PASSWORD']
    host = os.env['PERSONAL_DATA_DB_HOST']
    db = os.env['PERSONAL_DATA_DB_NAME']

    return mysql.connector.connect(user=usr,
                                password=pwd,
                                host=host,
                                database=db)


if __name__ == "main":
    """Main function for some reason"""
    db_data = get_db()
    db_query = db_data.cursor()
    db_query.execute('SELECT * FROM users;')

    for rows in db_query:
        print(''.join(str(rows)))
