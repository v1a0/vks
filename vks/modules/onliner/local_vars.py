from classes import APIBot
from classes import Database

""" Local module's variables
"""
users_ids: [str] = []
bot: APIBot
is_complete: bool = False
db: Database = Database(path='vks.db')
