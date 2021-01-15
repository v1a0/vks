import sqlite3
from flex_loger import logger
from typing import Dict, List, Iterable, Union, Any


class Database:
    @logger.catch
    def __init__(self, path: str = 'vks.db'):
        self.path: str = path  # path to or name of db
        with sqlite3.connect(self.path) as conn:
            self.cursor = conn.cursor()

    @logger.catch
    def execute(self, script: str):
        """
        Sent execute request to db
        :param script: SQLite script, for example: script = 'INSERT INTO table1 VALUES (1,2,3)'
        """
        with sqlite3.connect(self.path) as conn:
            self.cursor = conn.cursor()
            try:
                self.cursor.execute(script)
                conn.commit()
                return self.cursor.fetchall()
            except Exception as error:
                logger.error(error)

    @logger.catch
    def executemany(self, script: str, params: Iterable):
        """
        Sent executemany request to db
        :param script: SQLite script with placeholders, for example: script = 'INSERT INTO table1 VALUES (?,?,?)'
        :param params: Values for placeholders, for example: params = [ (1, 'text1', 0.1), (2, 'text2', 0.2) ]
        """
        with sqlite3.connect(self.path) as conn:
            self.cursor = conn.cursor()
            try:
                self.cursor.executemany(script, params)
                conn.commit()
            except Exception as error:
                logger.error(error)

    @logger.catch
    def executescript(self, script: str):
        """
        Sent executescript request to db
        :param script: SQLite script, for example: script = 'INSERT INTO table1 VALUES (1,2,3)'
        :return:
        """
        with sqlite3.connect(self.path) as conn:
            self.cursor = conn.cursor()
            try:
                self.cursor.executescript(script)
                conn.commit()
            except Exception as error:
                logger.error(error)

    @logger.catch
    def insert(self, table_name: str, rows: Dict[Any, Any]):
        """
        Insert data into db
        :param table_name = 'Table1'
        :param rows = {
                    'row1': 'value1',
                    '...':  '...',
                }
        """

        for (row, value) in rows.items():
            if type(value) == list:
                rows[row] = ','.join(map(str, value))  # map(str, value) stringifies list items

        columns = ', '.join(rows.keys())
        values = [tuple(rows.values())]
        placeholders = ", ".join("?" * len(rows.keys()))

        script = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.executemany(script, values)

    @logger.catch
    def select(self, table_name: str, select: List[str] = None, where: Dict[str, str] = None) -> List[Union[str]]:
        """
        Select data from db
        :param table_name = 'Table1'
        :param select = ['id', 'name']
        :param where = {
                    'row1': 'value1',
                    '...':  '...',
                }
        """

        where_data = where if where else {"'1'": '1'}
        select_data = select if select else ['*']

        _where_ = ''
        _select_ = ''

        for (row, val) in where_data.items():
            _where_ += f"{row}={val} AND " if type(val) == int else f"{row}='{val}' AND "

        for sel in select_data:
            _select_ += f"{sel}, "

        _where_ = _where_[:-5]
        _select_ = _select_[:-2]

        script = f"SELECT {_select_} FROM {table_name} WHERE {_where_}"
        return self.execute(script)

    @logger.catch
    def insert_or_replace(self, table_name: str, rows: Dict[str, str]):
        """
        Insert data or replace if it's already exist into db
        :param table_name = 'Table1'
        :param rows = {
                    'row1': 'rowvalue1',
                    '...':  '...',
                }
        """
        columns = ', '.join(rows.keys())
        values = [tuple(rows.values())]
        placeholders = ", ".join("?" * len(rows.keys()))
        script = f"INSERT OR REPLACE INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.executemany(script, values)

    @logger.catch
    def create_table(self, table_name: str, rows: Dict[str, str], foreign_keys: Dict[str, str] = None):
        """
        Create table in bd
        :param table_name = 'Table1'
        :param rows = {
                        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                        'user_id': 'INTEGER',
                        'name': 'TEXT',
                        '...' : '...',
        }
        :param foreign_keys = {
                'user_id': 'users("user_id")'
                '...' : '...',
        }
        """

        _rows_ = ''
        _foreign_keys_ = ''

        for (row, row_type) in rows.items():
            _rows_ += f'"{row}" {row_type},'
        _rows_ = _rows_[:-1]

        if foreign_keys:
            for (key, connection) in foreign_keys.items():
                _foreign_keys_ += f'FOREIGN KEY ("{key}") REFERENCES {connection},'

            _foreign_keys_ = _foreign_keys_[:-1]

        script = f"""
            PRAGMA _foreign_keys_=on;
            CREATE TABLE IF NOT EXISTS "{table_name}" (
            {_rows_}
            {',' if _foreign_keys_ else ''}
            {_foreign_keys_}
            );
            """

        self.executescript(script)
