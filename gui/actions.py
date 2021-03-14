"""
Файл с классом, реализующим вспомогательные действия (удаление, вывод данных в форму,
вывод окна с подтверждением выгрузки в файл, очистка форм)
"""

from PyQt5 import QtWidgets
from connection.connection import Connection


class Actions:
    """
    Класс действия. Экземпляр класса создается при запуске злавного окна приложения
    """
    def __init__(self, qtgui: any) -> None:
        """
        Метод init класса
        :param qtgui: экземпляр класса TkGUI (отрисовки основного окна)
        """
        self.gui = qtgui

    def position_output(self, pos_info: list) -> None:
        """
        Метод заполнения форм вкладки "Работа со штатным расписанием"
        :param pos_info: список с данными сотрудника
        :return: None
        """
        self.gui.form.department_input.setText(f'{pos_info[1]}')
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

    def clear_form(self) -> None:
        """
        Метод, очищающий формы ввода на вкладке "Работа со штатным расписанием"
        :return: None
        """
        self.gui.form.department_input.clear()
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

    def clear_stimul_form(self):
        self.gui.form.stimul_table.setRowCount(0)
        self.gui.form.message_label.clear()
        self.gui.form.save_stimul_table_button.setEnabled(False)

    def delete_confirmation(self) -> None:
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

    def save_confirmation(self, text: str, title: str) -> None:
        """
        Метод, запускающий информационное окно c результатом записи файла
        :param text: текст сообщения
        :param title: Название окна
        :return: None
        """
        msg = QtWidgets.QMessageBox(self.gui.window)
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec()
