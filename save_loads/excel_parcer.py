"""
Файл с вспомогательным классом, реализующим перенос штатного расписания в БД из формата Excel
"""
from pandas import read_excel
from connection.connection import SqliteDB
import settings


class ShtatExcelToDB:
    """
    Вспомогательный класс для загрузки данных сотрудников из файла формата Excel в БД
    """

    def __init__(self) -> None:
        """
        Метод инициализации класса. Считывает данные из файла, указанного в settings,
        переводит в формат списка
        """
        read = read_excel(f"../{settings.parcing_file}")
        self.res = read.values.tolist()
        self.db = SqliteDB()
        self.positions = {'na': "Руководитель",
                          'ws': "Вспомогательный рабочий",
                          'tt': "Технолог",
                          'sd': "Сдельщик",
                          'ti': "Повременщик",
                          'np': "непроизводственный персонал"}
        self.departments = {18000: "ЦРИЭГА",
                            20231: "ОТК",
                            33207: "Механический цех",
                            33208: "Монтажно-сборочный цех",
                            33209: "Каркасно-сборочный цех",
                            33210: "Гальвано-лакокрасочный цех",
                            33211: "Цех электронных устройств",
                            33218: "Механосборочный цех",
                            33219: "БИХ",
                            33300: "Ценовая группа",
                            33310: "Договорная группа",
                            33320: "Группа нормирования",
                            33340: "Плановая группа",
                            33410: "ОВК",
                            33420: "ОМТС",
                            33430: "ОПКиС",
                            33440: "БОЗД",
                            33511: "Отдел подготовки производства",
                            33512: "Цех инструментального хозяйства",
                            33513: "БИХ",
                            33520: "Отдел модернизации",
                            33600: "ПТД"
                            }

    def loader(self) -> None:
        """
        Метод непосредственно построчно записывает данные каждого сотрудника в БД
        :return: None
        """
        with self.db as cur:
            for item, value in enumerate(self.positions):
                cur.execute(f"INSERT INTO positions (position_code, position_name) "
                            f"VALUES ('{value}', '{self.positions[value]}');")
            for item, value in enumerate(self.departments):
                cur.execute(f"INSERT INTO departments (code, department) VALUES ({value},"
                            f" '{self.departments[value]}');")
            for i in self.res:
                print(i)
                cur.execute(f"INSERT INTO salaries "
                            f"(department_code, position, position_count, "
                            f"tarif, salary, fio, decree, history, decree_tarif, position_type) "
                            f"VALUES ('{i[0]}', '{i[1]}', '{i[2]}', '{i[3]}', '{i[4]}', '{i[5]}', "
                            f"'{i[6]}', '{i[7]}', '{i[8]}', '{i[9]}');")


if __name__ == '__main__':
    execute = ShtatExcelToDB()
    execute.loader()
