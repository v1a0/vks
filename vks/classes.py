import vk_api_lite as api
import sqlite3
from flex_loger import logger


class APIBot:
    @logger.catch
    def __init__(self, token: str, valid: bool, proxy=None):
        if proxy is None:
            proxy = {}
        self.token = token  # API token
        self.valid = valid  # is API token valid
        self.invalid = not valid  # is API token invalid
        self.proxy = proxy  # proxy settings
        self.method = ''  # method for request
        self.params = []  # parameters for request

    @logger.catch
    def request(self, method: str, params: dict) -> dict:
        return api.request(token=self.token, method=method, params=params, proxy=self.proxy)


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
            except Exception as error:
                logger.error(error)

    @logger.catch
    def executemany(self, script: str, params: list):
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
    def executescript(self, script):
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
    def insert(self, data: dict):
        """
        Insert data into db
        :param data: dict like down below
        {
            'table_name': 'Table1',
            'rows': {
                'id': '1',
                'user_id': '1234',
                'name': 'Username',
                '...' : '...',
            }
         }
        """
        columns = ', '.join(data.get('rows').keys())
        values = [tuple(data.get('rows').values())]
        placeholders = ", ".join("?" * len(data.get('rows').keys()))
        script = f"INSERT INTO {data.get('table_name')} ({columns}) VALUES ({placeholders})"
        self.executemany(script, values)

    @logger.catch
    def insert_or_replace(self, data: dict):
        """
        Insert data or replace if it's already exist into db
        :param data: dict like down below
        {
            'table_name': 'Table1',
            'rows': {
                'id': '1',
                'user_id': '1234',
                'name': 'Username',
                '...' : '...',
            }
         }
        """
        columns = ', '.join(data.get('rows').keys())
        values = [tuple(data.get('rows').values())]
        placeholders = ", ".join("?" * len(data.get('rows').keys()))
        script = f"INSERT OR REPLACE INTO {data.get('table_name')} ({columns}) VALUES ({placeholders})"
        self.executemany(script, values)

    @logger.catch
    def create_table(self, table: dict):
        """
        Create table in bd
        :param table: dict like down below
        {
            'table_name': 'table_name',
            'rows': {
                'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                'user_id': 'INTEGER',
                'name': 'TEXT',
                '...' : '...',
            },
            'foreign_keys': {
                'user_id': 'users("user_id")'
                '...' : '...',
            },
         }
        """

        if not table.get('rows') or not table.get('table_name'):
            return

        table_name = table.get('table_name')
        rows_dict = table.get('rows')
        foreign_keys_dict = table.get('foreign_keys')

        rows = ''
        for (row, row_type) in rows_dict.items():
            rows += f'"{row}" {row_type},'
        rows = rows[:-1]

        foreign_keys = ''
        if foreign_keys_dict:
            for (key, connection) in foreign_keys_dict.items():
                foreign_keys += f'FOREIGN KEY ("{key}") REFERENCES {connection},'

            foreign_keys = foreign_keys[:-1]

        script = f"""
            PRAGMA foreign_keys=on;
            CREATE TABLE IF NOT EXISTS "{table_name}" (
            {rows}
            {',' if foreign_keys else ''}
            {foreign_keys}
            );
            """

        self.executescript(script)
