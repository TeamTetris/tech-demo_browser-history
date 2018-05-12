import os
import shutil
import sqlite3
from pathlib import Path
from browser import Browser


class Chrome(Browser):

    def history_raw(self):
        if not self.is_installed():
            return {}

        # copy history database file to avoid locked database exception if chrome is currently running
        history_file_copy = Path("chrome_history")
        shutil.copy(str(self.__history_file__.absolute()), str(history_file_copy.absolute()))

        history = []
        db_connection = sqlite3.connect(str(history_file_copy.absolute()))

        try:
            db = db_connection.cursor()
            history = db.execute("SELECT url, visit_count FROM urls").fetchall()

        finally:
            db_connection.close()
            os.remove(str(history_file_copy.absolute()))

        return history

    def __history_file_windows__(self):
        local_appdata = os.getenv("%LOCALAPPDATA%")
        if not local_appdata:
            return Path()

        return Path(local_appdata).joinpath("Google/Chrome/User Data/Default/History")

    def __history_file_linux__(self):
        return Path(Path.home()).joinpath(".config/google-chrome/Default/History")

    def __history_file_mac__(self):
        return Path(Path.home()).joinpath("Library/Application Support/Google/Chrome/Default/History")
