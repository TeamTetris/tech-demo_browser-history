import os
import sqlite3
from browser import Browser
from pathlib import Path


class Firefox(Browser):

    @classmethod
    def __find_places__(cls, base_path):
        if not base_path.exists() or not base_path.is_dir():
            return Path()

        for file in base_path.iterdir():
            if not file.is_dir():
                continue

            if not str(file.absolute()).endswith(".default"):
                continue

            return file.joinpath("places.sqlite")

        return Path()

    def __history_raw__(self):
        if not self.is_installed():
            return []

        history_db = self.__copy_history_file__("firefox_history")
        history = []
        db_connection = sqlite3.connect(history_db)

        try:
            db = db_connection.cursor()
            history = db.execute("SELECT url, visit_count FROM moz_places WHERE visit_count > 0")\
                .fetchall()

        finally:
            db_connection.close()
            os.remove(history_db)

        return history

    def __history_file_windows__(self):
        app_data = os.getenv("%APPDATA%")
        if not app_data:
            print("%APPDATA% not found")
            return Path()

        return self.__find_places__(Path(app_data).joinpath("Mozilla/Firefox/Profiles"))

    def __history_file_linux__(self):
        return self.__find_places__(Path(Path.home()).joinpath(".mozilla/firefox"))

    def __history_file_mac__(self):
        return self.__find_places__(Path(Path.home()).joinpath("Library/Application Support/Firefox/Profiles"))
