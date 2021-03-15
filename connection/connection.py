import sqlite3
import settings
from abc import ABC, abstractmethod


class DatabaseContextManager(ABC):
    @abstractmethod
    def __init__(self, db_driver, config: dict):
        self.__db_driver = db_driver
        self.config = config

    def __enter__(self):
        self.conn = self.__db_driver.connect(**self.config)
        self.cursor = self.conn.cursor()
        self.__create_table()
        return self.cursor

    def __exit__(self, exc_type, exc_val, traceback):
        self.cursor.close()
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

    def __create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS salaries "
                            "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            "department_code INT NOT NULL, "
                            "position VARCHAR(45) NOT NULL, "
                            "position_count DECIMAL(10) NOT NULL, "
                            "tarif DECIMAL(10) NOT NULL, "
                            "salary DECIMAL(10) NOT NULL, "
                            "fio VARCHAR(100) NOT NULL, "
                            "decree TINYINT NULL, "
                            "history VARCHAR(255) NULL, "
                            "decree_tarif DECIMAL NULL, "
                            "position_type VARCHAR(2) NOT NULL);")
        self.conn.commit()


class SqliteDB(DatabaseContextManager):
    DEFAULT_DATABASE = settings.db_name
    DB_DRIVER = sqlite3

    def __init__(self, database=DEFAULT_DATABASE):
        config = {"database": database}
        super().__init__(self.DB_DRIVER, config)
