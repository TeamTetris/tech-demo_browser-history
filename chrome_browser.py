import os
import sqlite3
from pathlib import Path
from browser import Browser


class Chrome(Browser):

    def __history_raw__(self):
        if not self.is_installed():
            return []

        history_db = self.__copy_history_file__("chrome_history")
        history = []
        db_connection = sqlite3.connect(history_db)

        try:
            db = db_connection.cursor()
            history = db.execute("SELECT url, visit_count FROM urls WHERE visit_count > 0")\
                .fetchall()

        finally:
            db_connection.close()
            os.remove(history_db)

        return history

    def __history_file_windows__(self):
        local_app_data = os.getenv("LOCALAPPDATA")
        if not local_app_data:
            print("LOCALAPPDATA not found")
            return Path()

        return Path(local_app_data).joinpath("Google/Chrome/User Data/Default/History")

    def __history_file_linux__(self):
        return Path(Path.home()).joinpath(".config/google-chrome/Default/History")

    def __history_file_mac__(self):
        return Path(Path.home()).joinpath("Library/Application Support/Google/Chrome/Default/History")
