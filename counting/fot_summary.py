from connection import Connection
from counting.get_outs import Read_Outs


class FOT_summary:
    """
    Класс расчета размера стимулирующих надбавок и вывода результата в Table_View
    """

    def __init__(self, qtgui, fot, workdays, file):
        """
        Метод инициализации класса
        :param fot: Величина ФОТ к распределению
        :param workdays: Количество рабочих дней в месяце
        :param file: Файл с отклонениями
        """
        self.conn, self.cursor = Connection.connect()
        self.gui = qtgui
        self.fot = fot
        self.workdays = workdays
        self.file = file
        self.data = self.get_shtat_data()
        for i in range(0, len(self.data)):
            self.data[i] = list(self.data[i])
        self.code_list = []
        self.calculated = {}
        outs = Read_Outs(self.file)
        self.outs_list = outs.loader()
        self.outs = {}
        for i in self.outs_list:
            self.outs[i[0]] = [i[4], i[5], i[6]]

    def get_shtat_data(self):
        """
        Метод обращается к БД и получает список работающих (без вакансий и начальников)
        :return: self.cursor.fetchall() - список с данными работников
        """
        self.cursor.execute(f"SELECT * FROM salaries WHERE (fio NOT LIKE '%Вакансия%') "
                            f"AND (position_type NOT LIKE '%na%')")
        return self.cursor.fetchall()

    def get_department_dict(self):
        """
        Метод создает шаблон словаря для обобщения данных по подразделениям
        :return: None
        """
        for string in self.data:
            if string[1] not in self.calculated:
                self.code_list.append(string[1])
        for i in self.code_list:
            self.calculated[i] = {"pp_oklad": 0, "pp_stimul": 0,
                                  "np_oklad": 0, "np_stimul": 0,
                                  "tt_oklad": 0, "tt_stimul": 0,
                                  "fot_percent": 0}

    def calculate_oklads(self):
        """
        Метод, суммирующий окладную часть по подразделениям и добавляющий данные в словарь
        :return: None
        """
        self.get_department_dict()
        self.real_oklad_counting()
        for i in self.data:
            if i[10] == 'sd' or i[10] == 'ti':
                self.calculated[i[1]]["pp_oklad"] += float(round(i[5], 0))
            elif i[10] == 'np' or i[10] == 'ws':
                self.calculated[i[1]]["np_oklad"] += float(round(i[5], 0))
            else:
                self.calculated[i[1]]["tt_oklad"] += float(round(i[5], 0))

    def real_oklad_counting(self):
        """
        Метод расчитывает реальные оклады сотрудников с учетом отклонений
        и сохраняет их в список self.data
        :return: None
        """
        for i in self.data:
            if i[7] == 1:
                salary = i[9]
            else:
                salary = i[5]
            try:
                salary = round(salary / self.workdays * (self.workdays - self.outs[i[0]][0]
                                                         - self.outs[i[0]][1] - self.outs[i[0]][2]), 2)
                i[5] = salary
            except NameError:
                pass

    def calculate_percent(self) -> float:
        """
        Метод, расчитывающий коэффициент стимула для производственного персонала
        :return: fot_percent коэффициент стимула
        """
        summa = 0
        for i, v in enumerate(self.calculated):
            summa += self.calculated[v]['pp_oklad']
            summa += self.calculated[v]['tt_oklad']
        fot_percent = round(self.fot / summa - 1, 2)
        return fot_percent

    def calculate_stimul(self) -> dict:
        """
        Метод рассчитывает стимулирующую часть ФОТ и записывает результат для
        каждого подразделения в словарь
        :return: self.calculated - словарь с данными по ФОТ
        """
        self.calculate_oklads()
        stimul_percent = self.calculate_percent()
        for num, dep in enumerate(self.calculated):
            self.calculated[dep]['pp_stimul'] = round(self.calculated[dep]['pp_oklad'] * stimul_percent, 0)
            self.calculated[dep]['np_stimul'] = round(self.calculated[dep]['np_oklad'] * stimul_percent, 0)
            self.calculated[dep]['tt_stimul'] = round(self.calculated[dep]['tt_oklad'] * stimul_percent, 0)
            self.calculated[dep]['fot_percent'] = stimul_percent
        return self.calculated
