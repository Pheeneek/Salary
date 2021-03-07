from pandas import read_excel
from connection import Connection
import settings


class Shtat_Excel_To_DB:
    """
    Вспомогательный класс для загрузки данных сотрудников из файла формата Excel в БД
    """
    def __init__(self):
        """
        Метод инициализации класса. Считывает данные из файла, указанного в settings,
        переводит в формат списка
        """
        read = read_excel(settings.parcing_file)
        self.res = read.values.tolist()

    def loader(self):
        """
        Метод непосредственно построчно записывает данные каждого сотрудника в БД
        :return: None
        """
        con, cur = Connection.connect()
        for i in self.res:
            cur.execute(f"INSERT INTO salaries "
                        f"(department_code, position, position_count, "
                        f"tarif, salary, fio, decree, history, decree_tarif, position_type) "
                        f"VALUES ('{i[0]}', '{i[1]}', '{i[2]}', '{i[3]}', '{i[4]}', '{i[5]}', "
                        f"'{i[6]}', '{i[7]}', '{i[8]}', '{i[9]}');")
            con.commit()


if __name__ == '__main__':
    execute = Shtat_Excel_To_DB()
    execute.loader()
