# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from typing import Optional

import pytest
from sqlalchemy import text, inspect

LOGGER = logging.getLogger(__name__)

from . import conftest

FULL_ROWS = """[(1, 81297389127389213, Decimal('9112.229'), 9192.921875, 9292.17272, 'ZZZZZZZZZZZZ', b'AAAAAAAAA', datetime.datetime(2020, 4, 5, 15, 8, 39, 574000), datetime.date(2020, 4, 5)
, datetime.time(12, 19, 1), True), (2, 812123489127389213, Decimal('6782.229'), 2234193.0, 9122922.17272, 'BBBBBBBBB', b'CCCCCCCCCCCC', datetime.datetime(2020, 4, 5, 15, 8, 39, 574000), datetime.date(2022,
4, 5), datetime.time(10, 19, 1), False)]"""


@pytest.fixture(scope='session')
def engine():
    conftest.get_engine()
    return engine


def __execute(statement: str):
    engine = conftest.get_engine()
    with engine.connect() as conn:
        return conn.execute(text(statement))


def __has_table(table: str, schema: Optional[str] = None):
    engine = conftest.get_engine()
    with engine.connect() as conn:
        return inspect(engine).has_table(table, schema=schema)


def test_connect_args():
    """
    Tests connect string
    """
    engine = conftest.get_engine()
    try:
        results = __execute('select version from sys.version').fetchone()
        assert results is not None
    finally:
        engine.dispose()


def test_simple_sql():
    result = __execute('show databases')
    rows = [row for row in result]
    assert len(rows) >= 0, 'show database results'


def test_row_count(engine):
    rows = __execute('SELECT * FROM $scratch.sqlalchemy_tests').fetchall()
    assert len(rows) is 2


def test_has_table_true():
    assert __has_table("version", schema="sys")


def test_has_table_true2():
    assert __has_table("version")


def test_has_table_false():
    assert not __has_table("does_not_exist", schema="sys")


def test_has_table_false2():
    assert not __has_table("does_not_exist")
