import sqlite3
import settings
import logging


class Connection:
    @staticmethod
    def connect():
        con = sqlite3.connect(settings.db_name)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS salaries "
                    "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "department_code INT NOT NULL, "
                    "`position` VARCHAR(45) NOT NULL, "
                    "`position_count` DECIMAL(10) NOT NULL, "
                    "`tarif` DECIMAL(10) NOT NULL, "
                    "`salary` DECIMAL(10) NOT NULL, "
                    "`fio` VARCHAR(100) NOT NULL, "
                    "`decree` TINYINT NULL, "
                    "`history` VARCHAR(255) NULL, "
                    "`decree_tarif` DECIMAL NULL, "
                    "`position_type` VARCHAR(2) NOT NULL);")
        con.commit()
        logging.warning(f"Успешное подключение к базе данных '{settings.db_name}'!")
        return con

