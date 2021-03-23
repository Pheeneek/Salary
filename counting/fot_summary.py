"""
Файл с классом, непосредственно расчитывающим стимул с учетом отклонений
"""
from connection.connection import SqliteDB
from ..counting.get_outs import ReadOuts


class FOTSummary:
    """
    Класс расчета размера стимулирующих надбавок
    """

    def __init__(self, qtgui: any, fot: int, workdays: int, file: str) -> None:
        """
        Метод инициализации класса
        :param fot: Величина ФОТ к распределению
        :param workdays: Количество рабочих дней в месяце
        :param file: Файл с отклонениями
        """
        self.db = SqliteDB()
        self.gui = qtgui
        self.fot = fot
        self.workdays = workdays
        self.file = file
        self.data = self.get_shtat_data()
        for i in range(0, len(self.data)):
            self.data[i] = list(self.data[i])
        self.code_list = []
        self.calculated = {}
        outs = ReadOuts(self.file)
        self.outs_list = outs.loader()
        self.outs = {}
        for i in self.outs_list:
            self.outs[i[0]] = [i[4], i[5], i[6]]

    def get_shtat_data(self) -> list:
        """
        Метод обращается к БД и получает список работающих (без вакансий и начальников)
        :return: cursor.fetchall() - список с данными работников
        """
        with self.db as cursor:
            cursor.execute(f"SELECT * FROM salaries WHERE (fio NOT LIKE '%Вакансия%') "
                           f"AND (position_type NOT LIKE '%na%')")
            return cursor.fetchall()

    def get_department_dict(self) -> None:
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

    def calculate_oklads(self) -> None:
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

    def real_oklad_counting(self) -> None:
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
                salary = round(salary / self.workdays * (self.workdays - self.outs[i[0]][0] -
                               self.outs[i[0]][1] - self.outs[i[0]][2]), 2)
                i[5] = salary
            except (NameError, KeyError, TypeError):
                pass

    def calculate_percent(self) -> [float, float]:
        """
        Метод, расчитывающий коэффициент стимула для производственного персонала
        :return: fot_percent коэффициент стимула
        """
        summa_oklad = 0
        for i, v in enumerate(self.calculated):
            summa_oklad += self.calculated[v]['pp_oklad']
            summa_oklad += self.calculated[v]['tt_oklad']
        fot_percent = round(self.fot / summa_oklad - 1, 2)
        return fot_percent, summa_oklad

    def calculate_stimul(self) -> [dict, float]:
        """
        Метод рассчитывает стимулирующую часть ФОТ и записывает результат для
        каждого подразделения в словарь. Если процент стимула указан явно - использует его,
        иначе использует общий процент
        :return: self.calculated - словарь с данными по ФОТ
        """
        self.calculate_oklads()
        stimul_percent, summa = self.calculate_percent()
        for num, dep in enumerate(self.calculated):
            if dep == 18000:
                if self.gui.form.stimul_input_gidr.text():
                    self.calculated[dep]['fot_percent'] = float(str(self.gui.form.stimul_input_gidr.text())
                                                                .replace(",", "."))
                else:
                    self.calculated[dep]['fot_percent'] = stimul_percent
            elif dep == 33600:
                if self.gui.form.stimul_input_ptd.text():
                    self.calculated[dep]['fot_percent'] = float(str(self.gui.form.stimul_input_ptd.text())
                                                                .replace(",", "."))
                else:
                    self.calculated[dep]['fot_percent'] = stimul_percent
            else:
                if self.gui.form.stimul_input_prk.text():
                    self.calculated[dep]['fot_percent'] = float(str(self.gui.form.stimul_input_prk.text())
                                                                .replace(",", "."))
                else:
                    self.calculated[dep]['fot_percent'] = stimul_percent
            self.calculated[dep]['pp_stimul'] = round(self.calculated[dep]['pp_oklad'] *
                                                      self.calculated[dep]['fot_percent'], 0)
            self.calculated[dep]['np_stimul'] = round(self.calculated[dep]['np_oklad'] *
                                                      self.calculated[dep]['fot_percent'], 0)
            self.calculated[dep]['tt_stimul'] = round(self.calculated[dep]['tt_oklad'] *
                                                      self.calculated[dep]['fot_percent'], 0)
            summa += self.calculated[dep]['tt_stimul']
            summa += self.calculated[dep]['pp_stimul']
        return self.calculated, summa
