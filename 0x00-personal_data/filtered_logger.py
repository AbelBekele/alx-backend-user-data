#!/usr/bin/env python3
"""
    Obfuscated and replace with regex
    Provide Log formatter
    Create logger
"""
import os
import logging
import mysql.connector
from re import sub
from typing import List, Tuple


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Get a point of connection toward the database

        Return:
            A connection toward the database
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    passw = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    hosting = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db = os.getenv('PERSONAL_DATA_DB_NAME')

    medb = mysql.connector.connect(
        host=hosting,
        username=username,
        password=passw,
        database=db
    )

    return medb


def get_logger() -> logging.Logger:
    """Set the format of the record

        Return:
            The function overloaded to make a new log with all items
    """
    log: logging.Logger = logging.getLogger('user_data')
    log.propagate = False

    stream_handler: logging.StreamHandler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    formatter = logging.Formatter((RedactingFormatter(fields=PII_FIELDS)))
    stream_handler.formatter(formatter)

    log.addHandler(stream_handler)

    return log


def filter_datum(fields: List, redaction: str,
                 message: str, separator: str) -> str:
    """
        Filter and obfuscated the string

        Args:
            fields: a list of strings representing all fields to obfuscate
                    ["password", "date_of_birth"]
            redaction: a string representing by what the
                       field will be obfuscated
                       "XXXXX"
            message: a string representing the log line
                    ["name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;"]
                    ["name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"]
            separator: a string representing by which character is
                    separating all fields in the log line (message)
                    ";"
        Return:
            String with string ofuscated
    """
    for field in fields:
        message = sub(f'{field}=.+?{separator}',
                      f'{field}={redaction}{separator}', message)

    return message


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
            Set the format of the record

            Args:
                record: Log record of a event

            Return:
                The function overloaded to make a new log with all items
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)

        return (super(RedactingFormatter, self).format(record))


def main():
    """Entry Point"""
    db: mysql.connector.connection.MySQLConnection = get_db()
    cursor = db.cursor()
    headers: Tuple = (head[0] for head in cursor.description)
    cursor.execute("SELECT name, email, phone, ssn, password FROM users;")
    log: logging.Logger = get_logger()

    for row in cursor:
        """ zip Element combine two tuples to generate
            a new tuple combined
        """
        for row in cursor:
            data_row: str = ''
            for key, value in zip(headers, row):
                data_row = ''.join(f'{key}={str(value)};')

            log.info(data_row)

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
