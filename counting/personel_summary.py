"""
Файл с классом, расчитывающим текущую численность по категориям и подразделениям
"""

from connection.connection import SqliteDB


class PersonelSummary:
    """
    Класс, рассчитывающий общую численность персонала по категориям
    """
    def __init__(self) -> None:
        """
        Метод инициализации класса
        """
        self.db = SqliteDB()
        self.code_list = []
        self.data = self.get_data()
        self.data_for_table = {}

    def get_data(self) -> tuple:
        """
        Метод, получающий из БД данные о всех записях
        :return: self.cur.fetchall() - список с результами запроса
        """
        with self.db as cur:
            cur.execute("SELECT * FROM salaries")
        return cur.fetchall()

    def get_department_dict(self) -> None:
        """
        Метод создает словарь с ключами - названиями подразделений
        :return: None
        """
        for string in self.data:
            if string[1] not in self.code_list:
                self.code_list.append(string[1])
        for i in self.code_list:
            self.data_for_table[i] = {"pp": {"sdelka": 0, "vremya": 0, "tech": 0, "summary": 0},
                                      "np": {"specialist": 0, "worker": 0, "summary": 0}}

    def data_counting(self) -> dict:
        """
        Метод заполняющий словарь по численности в разрезе подразделений и категорий сотрудников
        :return: self.data_for_table - словарь с данными о численности по подразделениям
        и категориям работников
        """
        self.get_department_dict()
        for pos in self.data:
            if pos[6] != "Вакансия" and pos[7] != 1:
                if pos[10] == "sd":
                    self.data_for_table[pos[1]]["pp"]["sdelka"] += 1
                    self.data_for_table[pos[1]]["pp"]["summary"] += 1
                elif pos[10] == "ti":
                    self.data_for_table[pos[1]]["pp"]["vremya"] += 1
                    self.data_for_table[pos[1]]["pp"]["summary"] += 1
                elif pos[10] == "np" or pos[10] == "na":
                    self.data_for_table[pos[1]]["np"]["specialist"] += 1
                    self.data_for_table[pos[1]]["np"]["summary"] += 1
                elif pos[10] == "ws":
                    self.data_for_table[pos[1]]["np"]["worker"] += 1
                    self.data_for_table[pos[1]]["np"]["summary"] += 1
                elif pos[10] == "tt":
                    self.data_for_table[pos[1]]["pp"]["tech"] += 1
                    self.data_for_table[pos[1]]["pp"]["summary"] += 1
        return self.data_for_table
