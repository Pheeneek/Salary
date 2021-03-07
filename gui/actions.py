import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from connection import Connection
from counting.fot_summary import FOT_summary


class Actions:
    """
    Класс действия. Экземпляр класса создается при запуске злавного окна приложения
    """
    def __init__(self, qtgui):
        """
        Метод init класса
        :param qtgui: экземпляр класса TkGUI (отрисовки основного окна)
        """
        self.gui = qtgui

    def position_output(self, pos_info):
        """
        Метод заполнения форм вкладки "Работа со штатным расписанием"
        :param pos_info: список с данными сотрудника
        :return: None
        """
        self.gui.form.department_input.setCurrentText(f'{pos_info[1]}')
        self.gui.form.pos_input.setText(f'{pos_info[2]}')
        self.gui.form.pos_count_input.setText(f'{pos_info[3]}')
        self.gui.form.fio_input.setText(f'{pos_info[6]}')
        self.gui.form.tarif_input.setText(f'{pos_info[4]}')
        self.gui.form.salary_input.setText(f'{pos_info[5]}')
        if pos_info[8] != '0':
            self.gui.form.history_text.setText(f'{pos_info[8]}')
        else:
            self.gui.form.history_text.clear()
        if pos_info[10] == 'na':
            self.gui.form.na.setChecked(True)
        elif pos_info[10] == 'tt':
            self.gui.form.tt.setChecked(True)
        elif pos_info[10] == 'sd':
            self.gui.form.sd.setChecked(True)
        elif pos_info[10] == 'ws':
            self.gui.form.ws.setChecked(True)
        elif pos_info[10] == 'ti':
            self.gui.form.ti.setChecked(True)
        else:
            self.gui.form.np.setChecked(True)
        if pos_info[7] == 1:
            self.gui.form.do_y_n.setChecked(True)
            self.gui.form.do_salary_input.setText(f"{pos_info[8]}")
        else:
            self.gui.form.do_y_n.setChecked(False)
            self.gui.form.do_salary_input.clear()

    def make_changes(self):
        pass  # TODO доделать изменения

    def clear_form(self):
        """
        Метод, очищающий формы ввода на вкладке "Работа со штатным расписанием"
        :return: None
        """
        self.gui.form.department_input.setCurrentIndex(0)
        self.gui.form.pos_input.clear()
        self.gui.form.pos_count_input.clear()
        self.gui.form.fio_input.clear()
        self.gui.form.tarif_input.clear()
        self.gui.form.salary_input.clear()
        self.gui.form.do_y_n.setChecked(False)
        self.gui.form.do_salary_input.clear()
        self.gui.form.vacancy.setChecked(False)
        self.gui.form.history_text.clear()
        self.gui.form.search_number.setText(f"Позиция : 0 из 0")
        self.gui.form.left_button.setEnabled(False)
        self.gui.form.right_button.setEnabled(False)
        self.gui.form.delete_button.setEnabled(False)
        self.gui.form.save_button.setEnabled(False)

    def delete_confirmation(self):
        """
        Метод, запускающий окно подтверждения удаления текущей позиции из штатного расписания
        :return: None
        """
        message = f'Вы уверены, что хотите удалить штатную единицу ' \
                  f'"{self.gui.search[self.gui.current_position - 1][2]}"? '
        reply = QtWidgets.QMessageBox.question(self.gui.window, 'Удаление штатной единицы', message,
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            conn, cursor = Connection.connect()
            cursor.execute(f"DELETE FROM salaries WHERE id = '{self.gui.search[self.gui.current_position - 1][0]}';")
            conn.commit()
            self.clear_form()


class Count_stimul_data:
    """
    Класс расчета стимула и выводящий результаты расчета в Table_View
    """
    def __init__(self, qtgui, file):
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
            self.fot_summary = FOT_summary(self.gui, self.fot, self.workdays, self.file)
            self.main_data = self.fot_summary.calculate_stimul()
            self.data_list = []
            self.stimul_to_list()
            self.print_results()

    def stimul_to_list(self):
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

    def print_results(self):
        """
        Метод вывода результатов расчетов в Table_View
        :return: None
        """
        self.gui.form.stimul_table.setRowCount(len(self.data_list))
        self.gui.form.stimul_table.setColumnCount(8)
        self.gui.form.stimul_table.setHorizontalHeaderLabels(['Подразделение', 'ПП оклады', 'ПП стимул',
                                                              'НП оклады', 'НП стимул',
                                                              'Технологи оклады', 'Технологи стимул', 'Процент'])
        for i in range(0, len(self.data_list)):
            for j in range(0, 8):
                item = QTableWidgetItem(str(self.data_list[i][j]))
                self.gui.form.stimul_table.setItem(i, j, item)
        self.gui.form.stimul_table.resizeColumnsToContents()

    def verify_counting_data(self):
        """
         Метод, запускающий проверки на валидность данных для расчета
         :return: True, если проверки пройдены
                  False, если хоть одна проверка провалена
         """
        if self.verify_ints(self.gui.form.fot_input.text()) \
                and self.verify_ints(self.gui.form.workday_input.text()) \
                and self.verify_path():
            return True
        else:
            return False

    def verify_ints(self, value):
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

    def verify_path(self):
        """
        Метод проверяет наличие пути, указанного в полу file_input
        :return: True, если путь существует
                 False, если указанного пути нет
        """
        if os.path.exists(self.gui.form.file_input.text()):
            return True
        else:
            self.gui.form.message_label.setText("Файл отклонений не найден!")
            return False
