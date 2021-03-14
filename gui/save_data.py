"""
Класс, реализующий сохранение новой позиции в БД
"""
from PyQt5 import QtWidgets
from connection.connection import Connection


class Save_data:
    """
    Класс сохранения данных сотрудника в БД
    """
    def __init__(self, qtgui: any) -> None:
        """
        Метод init класса. Считывает данные из полей ввода
        :param qtgui: экземпляр класса TkGUI (отрисовки основного окна)
        """
        self.gui = qtgui
        self.con, self.cursor = Connection.connect()
        self.department = self.gui.form.department_input.text()
        self.position = self.gui.form.pos_input.text()
        self.fio = self.gui.form.fio_input.text()
        self.tarif = self.gui.form.tarif_input.text()
        self.salary = self.gui.form.salary_input.text()
        self.pos_count = self.gui.form.pos_count_input.text()
        self.history = self.gui.form.history_text.toPlainText()
        if self.gui.form.na.isChecked():
            self.position_type = 'na'
        elif self.gui.form.ws.isChecked():
            self.position_type = 'ws'
        elif self.gui.form.ti.isChecked():
            self.position_type = 'ti'
        elif self.gui.form.ws.isChecked():
            self.position_type = 'ws'
        elif self.gui.form.np.isChecked():
            self.position_type = 'np'
        else:
            self.position_type = 'tt'
        if self.gui.form.do_y_n.isChecked():
            self.decree = 1
            self.decree_tarif = self.gui.form.do_salary_input.text()
        else:
            self.decree = 0
            self.decree_tarif = "0"

    def save(self) -> None:
        """
        Метод, осуществляющий попытку записи данных сотрудников в БД
        :return: None
        """
        if self.verify_data():
            try:
                self.cursor.execute(f"INSERT INTO salaries (department_code, position, position_count, "
                                    f"tarif, salary, fio, decree, history, decree_tarif, position_type) "
                                    f"VALUES ('{self.department}', '{self.position}', '{self.pos_count}', "
                                    f"'{self.tarif}', '{self.salary}', '{self.fio}', '{self.decree}', "
                                    f"'{self.history}', '{self.decree_tarif}', '{self.position_type}');")
                self.con.commit()
                self.gui.form.save_button.setEnabled(False)
                self.save_confirmation()
            except NameError:
                print("Ошибка записи в базу!!!")

    def save_confirmation(self) -> None:
        """
        Метод, запускающий информационное окно, если позиция удачно записана в базу
        :return: None
        """
        msg = QtWidgets.QMessageBox(self.gui.window)
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Позиция упешно добавлена в базу!")
        msg.setWindowTitle("Сохранение позиции")
        msg.exec()

    def verify_data(self) -> bool:
        """
        Метод, запускающий проверки числовых значений на валидность
        :return: True, если проверки пройдены
                 False, если хоть одна проверка провалена
        """
        if self.verify_ints(self.tarif) \
                and self.verify_ints(self.salary) \
                and self.verify_ints(self.pos_count) \
                and self.verify_ints(self.decree_tarif):
            return True
        else:
            return False

    def verify_ints(self, value: str) -> bool:
        """
        Метод проверки значения на неотрицательность и что оно является числом
        :param value: проверяемое значение
        :return: True, если проверка пройдена
                 False, еслм проверка провалена
        """
        try:
            value = int(value)
            if 0 > value:
                self.gui.form.search_number.setText("Отрицательное значение данных!")
                return False
        except ValueError:
            self.gui.form.search_number.setText("Ошибка вводимых данных!")
            return False
        return True
