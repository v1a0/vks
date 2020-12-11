from classes import APIBot

""" Local module's variables
NECESSARY VARIABLES FOR ANY MODULE
"""
users_ids: [str] = []       # List of users to handle with
bot: APIBot                 # Bot for API requests
is_complete: bool = False   # Is module successfully complete
timeout: float = 60         # Timeout for module usage (how often module have to be executed)
ready_after: float = 0      # Necessary var, just don't touch it, ok?


""" 
Custom variables of module
"""