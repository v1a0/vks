import sqlite3
from loguru import logger


@logger.catch
def db_execute(sqlite_script):
    """
    Sent execute request to db
    :param sqlite_script: str
    :return:
    """

    with sqlite3.connect('vks.db') as conn:
        conn.cursor().executescript(sqlite_script)


@logger.catch
def insert_and_update_user_data(uid, time, first_name, last_name, is_closed, online, sex, photo, mobile, os):
    """
    Inserting users data into db if user not exist and updating if user already exist
    :param uid: int
    :param time: str
    :param first_name: str
    :param last_name: str
    :param is_closed: bool
    :param online: int
    :param sex: int
    :param photo: str
    :param mobile: int
    :return:
    """

    insert_req = f"""
    INSERT OR REPLACE INTO users (user_id,first_name,last_name,is_closed,sex,photo) VALUES
    ((SELECT user_id FROM users WHERE user_id = {uid}), '{first_name}', '{last_name}', '{is_closed}', {sex}, '{photo}');
    
    INSERT INTO logging (time,user_id,online,mobile,os) 
    VALUES ('{time}', {uid}, {online}, {mobile}, '{os}');
    """

    db_execute(insert_req)


@logger.catch
def db_structure_controller():

    crate_tables_req = """
                PRAGMA foreign_keys=on;
     
                CREATE TABLE IF NOT EXISTS "logging" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time TEXT,
                "user_id"   INTEGER,
                "online"	INTEGER,
                "mobile"	INTEGER,
                "os"	TEXT,
                FOREIGN KEY ("user_id") REFERENCES users("user_id")
                );
                
                CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                first_name TEXT,
                last_name TEXT,
                is_closed TEXT,
                sex INTEGER,
                photo TEXT            
                );
                """

    db_execute(crate_tables_req)


db_structure_controller()
