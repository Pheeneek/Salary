"""
Файл с классом запуска расчета и вывода таблицы с результатами
"""
import os
from PyQt5.QtWidgets import QTableWidgetItem
from ..counting.fot_summary import FOTSummary


class CountStimulData:
    """
    Класс расчета стимула и выводящий результаты расчета в Table_View
    """

    def __init__(self, qtgui: any, file: str) -> None:
        """
        Метод init класса
        :param qtgui: экземпляр класса TkGUI (отрисовки основного окна)
               file: файл для загрузки отклонений
        """
        self.gui = qtgui
        self.file = file
        if self.verify_counting_data():
            self.fot = int(self.gui.form.fot_input.text())
            self.workdays = int(self.gui.form.workday_input.text())
            self.fot_summary = FOTSummary(self.gui, self.fot, self.workdays, self.file)
            self.main_data, self.summa = self.fot_summary.calculate_stimul()
            self.data_list = []
            self.stimul_to_list()
            self.print_results()

    def stimul_to_list(self) -> None:
        """
        Метод переводит данные по подразделениям из словаря в сортированный список
        для дальнейшего вывода в Table_View
        :return: None
        """
        for item, v in enumerate(self.main_data):
            self.data_list.append([v, self.main_data[v]['pp_oklad'], self.main_data[v]['pp_stimul'],
                                   self.main_data[v]['np_oklad'], self.main_data[v]['np_stimul'],
                                   self.main_data[v]['tt_oklad'], self.main_data[v]['tt_stimul'],
                                   self.main_data[v]['fot_percent']])
        self.data_list.sort()

    def print_results(self) -> None:
        """
        Метод вывода результатов расчетов в Table_View
        :return: None
        """
        self.gui.form.stimul_table.setRowCount(len(self.data_list))
        for i in range(0, len(self.data_list)):
            for j in range(0, 8):
                item = QTableWidgetItem(str(self.data_list[i][j]))
                self.gui.form.stimul_table.setItem(i, j, item)
        self.gui.form.stimul_table.resizeColumnsToContents()

    def verify_counting_data(self) -> bool:
        """
         Метод, запускающий проверки на валидность данных для расчета
         :return: True, если проверки пройдены
                  False, если хоть одна проверка провалена
         """
        return bool(self.verify_path()
                    and self.verify_ints(self.gui.form.workday_input.text())
                    and self.verify_ints(self.gui.form.fot_input.text()))

    def verify_ints(self, value: str) -> bool:
        """
        Метод проверки значения на неотрицательность и что оно является числом
        :param value: проверяемое значение
        :return: True, если проверка пройдена
                 False, еслм проверка провалена
        """
        try:
            value = int(value)
            if value <= 0:
                self.gui.form.message_label.setText("Неверное значение данных для расчета!")
                return False
        except ValueError:
            self.gui.form.message_label.setText("Ошибка вводимых данных!")
            return False
        return True

    def verify_path(self) -> bool:
        """
        Метод проверяет наличие пути, указанного в полу file_input
        :return: True, если путь существует
                 False, если указанного пути нет
        """
        if os.path.exists(self.gui.form.file_input.text()):
            return True
        self.gui.form.message_label.setText("Файл отклонений не найден!")
        return False
