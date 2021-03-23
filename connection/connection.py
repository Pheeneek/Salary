"""
Модуль для соединения с БД
"""
from abc import ABC, abstractmethod
import sqlite3
import settings


class DatabaseContextManager(ABC):
    """
    Общий класс для всех соединений
    """

    @abstractmethod
    def __init__(self, db_driver, config: dict) -> None:
        """
        Метод инициализации класса
        :param db_driver: драйвер для работы с БД
        :param config: словарь с конфигурацией для создания содинения с БД
        """
        self.__db_driver = db_driver
        self.config = config
        self.conn = self.__db_driver.connect(**self.config)
        self.cursor = self.conn.cursor()

    def __enter__(self) -> any:
        """
        Метод подключения к БД, запускает метод создания таблицы salaries
        :return: self.cursor - курсор для работы с БД
        """
        self.__create_table()
        return self.cursor

    def __exit__(self, exc_type: any, exc_val: any, traceback: any) -> None:
        """
        Метод закрывающий соединение.
        :param exc_type: если параметр не None, откатывает изменения в БД
        :param exc_val:
        :param traceback:
        :return: None
        """
        self.cursor.close()
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

    def __create_table(self) -> None:
        """
        Метод создает таблицу salaries в БД, если ее не существует
        :return: None
        """
        self.cursor.execute("CREATE TABLE IF NOT EXISTS departments "
                            "(code INTEGER PRIMARY KEY, "
                            "department VARCHAR(50));")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS positions "
                            "(position_code VARCHAR(2) PRIMARY KEY, "
                            "position_name VARCHAR(50));")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS salaries "
                            "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            "department_code INT, "
                            "position VARCHAR(45) NOT NULL, "
                            "position_count DECIMAL(10) NOT NULL, "
                            "tarif DECIMAL(10) NOT NULL, "
                            "salary DECIMAL(10) NOT NULL, "
                            "fio VARCHAR(100) NOT NULL, "
                            "decree TINYINT NULL, "
                            "history VARCHAR(255) NULL, "
                            "decree_tarif DECIMAL NULL, "
                            "position_type VARCHAR(2), "
                            "FOREIGN KEY (position_type) "
                            "REFERENCES positions (position_type), "
                            "FOREIGN KEY (department_code) "
                            "REFERENCES departments (code));")
        self.conn.commit()


class SqliteDB(DatabaseContextManager):
    """
    Конкретный класс для работы с БД с помощью драйвера sqlite3
    """
    DEFAULT_DATABASE = settings.db_name
    DB_DRIVER = sqlite3

    def __init__(self, database: str = DEFAULT_DATABASE) -> None:
        """
        метод инициализации класса
        :param database: файл с БД
        """
        config = {"database": database}
        super().__init__(self.DB_DRIVER, config)
