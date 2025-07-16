from helpers.config import get_settings, Settings
import os
import random
import string

class BaseController:
    

    def __init__(self):
        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.files_dir = os.path.join(
            self.base_dir,
            'assets/files'
            )
        
        self.database_dir = os.path.join(
            self.base_dir,
            'assets/database'
            )
        
    def generate_random_string(self, length: int = 10) -> str:
        """
        Generate a random string of fixed length.
        """
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(length))
    
    def get_database_path(self, db_name: str) -> str:
        """
        Get the full path for a database file.
        """
        database_path = os.path.join(
            self.database_dir, db_name
        )
        
        if not os.path.exists(database_path):   
            os.makedirs(database_path)
        
        return database_path