from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from connection import Connection
from fot_summary import FOT_summary
from shtat_to_excel import Shtat_To_Excel


class Search:
    def __init__(self, qtgui):
        self.gui = qtgui
        self.search, self.current_position = [], 0
        self.con = Connection.connect()
        self.department = self.gui.form.department_input.currentText()
        self.position = self.gui.form.pos_input.text()
        self.fio = self.gui.form.fio_input.text()
        self.tarif = self.gui.form.tarif_input.text()
        self.salary = self.gui.form.salary_input.text()
        self.pos_count = self.gui.form.pos_count_input.text()
        cursor = self.con.cursor()
        try:
            cursor.execute(f"SELECT * FROM salaries WHERE "
                           f"(department_code LIKE '%{self.department}%') AND "
                           f"(position LIKE '%{self.position}%') AND "
                           f"(fio LIKE '%{self.fio}%') AND "
                           f"(tarif LIKE '%{self.tarif}%') AND "
                           f"(salary LIKE '%{self.salary}%') AND "
                           f"(position_count LIKE '%{self.pos_count}%');")
            self.search_result = cursor.fetchall()
        except:
            pass

    def search_clicked(self):
        if self.search_result and len(self.search_result) > 0:
            self.gui.form.search_number.setText(f"Позиция : {1} из {len(self.search_result)}")
            self.gui.form.delete_button.setEnabled(True)
            if len(self.search_result) > 1:
                self.gui.form.right_button.setEnabled(True)
            else:
                self.gui.form.right_button.setEnabled(False)
        else:
            self.gui.form.search_number.setText(f"Позиция : {0} из {0}")
        if self.search_result:
            self.gui.actions.position_output(self.search_result[0])
            return self.search_result


class Actions:
    def __init__(self, qtgui):
        self.gui = qtgui

    def set_save(self):
        self.gui.form.save_button.setEnabled(True)

    def position_output(self, pos_info):
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
        self.make_changes()

    def make_changes(self):
        pass

    def clear_form(self):
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
        message = f'Вы уверены, что хотите удалить штатную единицу "{self.gui.search[self.gui.current_position - 1][2]}"?'
        reply = QtWidgets.QMessageBox.question(self.gui.window, 'Удаление штатной единицы', message,
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            conn = Connection.connect()
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM salaries WHERE id = '{self.gui.search[self.gui.current_position - 1][0]}';")
            conn.commit()
            self.clear_form()


class Save_data:
    def __init__(self, qtgui):
        self.gui = qtgui
        self.con = Connection.connect()
        self.department = self.gui.form.department_input.currentText()
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
            self.decree_tarif = gui.form.do_salary_input.text()
        else:
            self.decree = 0
            self.decree_tarif = "0"

    def save(self):
        cursor = self.con.cursor()
        try:
            cursor.execute(f"INSERT INTO salaries (department_code, position, position_count, "
                           f"tarif, salary, fio, decree, history, decree_tarif, position_type) "
                           f"VALUES ('{self.department}', '{self.position}', '{self.pos_count}', "
                           f"'{self.tarif}', '{self.salary}', '{self.fio}', '{self.decree}', "
                           f"'{self.history}', '{self.decree_tarif}', '{self.position_type}');")
            self.con.commit()
            self.gui.form.save_button.setEnabled(False)
            self.save_confirmation()
        except NameError:
            print("Ошибка записи в базу!!!")

    def save_confirmation(self):
        msg = QtWidgets.QMessageBox(self.gui.window)
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Позиция упешно добавлена в базу!")
        msg.setWindowTitle("Сохранение позиции")
        msg.exec()

    def verify_data(self):
        pass  # TODO Сделать проверку вводимых данных на валидность


class Count_stimul_data:
    def __init__(self, qtgui):
        self.gui = qtgui
        self.fot = int(self.gui.form.fot_input.text())
        self.workdays = int(self.gui.form.workday_input.text())
        self.fot_summary = FOT_summary(self.fot, self.workdays)
        self.main_data = self.fot_summary.calculate_stimul()
        self.data_list = []
        self.stimul_to_list()
        self.print_results()

    def stimul_to_list(self):
        for item, v in enumerate(self.main_data):
            self.data_list.append([v, self.main_data[v]['pp_oklad'], self.main_data[v]['pp_stimul'],
                                   self.main_data[v]['np_oklad'], self.main_data[v]['np_stimul'],
                                   self.main_data[v]['tt_oklad'], self.main_data[v]['tt_stimul'],
                                   self.main_data[v]['fot_percent']])
        self.data_list.sort()

    def print_results(self):

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
    # ------------ Основной код ----------------


class Gui:
    def __init__(self):

        self.actions = Actions(self)
        months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль",
                  "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        departments = []
        con = Connection.connect()
        cur = con.cursor()
        cur.execute("SELECT DISTINCT department_code FROM salaries ORDER BY department_code;")
        for i in cur.fetchall():
            departments.append(str(i[0]))
        # Определение и запуск основного окна интерфейса

        Form, Window = uic.loadUiType("MainWindow.ui")

        app = QApplication([])
        self.window = Window()
        self.form = Form()
        self.form.setupUi(self.window)
        self.window.show()

        # Определение начальных состояний и действий кнопок

        self.form.search_button.clicked.connect(self.search_button)
        self.form.clear_form_buton.clicked.connect(self.clear_button)
        self.form.right_button.clicked.connect(self.right_button)
        self.form.left_button.clicked.connect(self.left_button)
        self.form.new_position_button.clicked.connect(self.new_position_button)
        self.form.delete_button.clicked.connect(self.delete_button)
        self.form.save_button.clicked.connect(self.save_button)
        self.form.save_shtat_table.clicked.connect(self.save_shtat_table_button)
        self.form.count_button.clicked.connect(self.count_button)

        self.form.left_button.setEnabled(False)
        self.form.right_button.setEnabled(False)
        self.form.save_button.setEnabled(False)
        self.form.delete_button.setEnabled(False)
        self.form.cancel_button.setEnabled(False)

        self.form.month.addItems(months)
        self.form.department_input.addItems(departments)
        # Запуск цикла

        self.search = []
        self.current_position = 1
        app.exec()

    def search_button(self):
        search_result = Search(self)
        self.search = search_result.search_clicked()

    def clear_button(self):
        self.actions.clear_form()

    def right_button(self):
        self.form.left_button.setEnabled(True)
        self.current_position += 1
        self.form.search_number.setText(f"Позиция : {self.current_position} из {len(self.search)}")
        if self.current_position >= len(self.search):
            self.form.right_button.setEnabled(False)
        self.actions.position_output(self.search[self.current_position - 1])

    def left_button(self):
        self.form.right_button.setEnabled(True)
        self.current_position -= 1
        self.form.search_number.setText(f"Позиция : {self.current_position} из {len(self.search)}")
        if self.current_position <= 1:
            self.form.left_button.setEnabled(False)
        self.actions.position_output(self.search[self.current_position - 1])

    def new_position_button(self):
        self.actions.clear_form()
        self.form.save_button.setEnabled(True)

    def delete_button(self):
        self.actions.delete_confirmation()

    def save_button(self):
        pos_data = Save_data(self)
        pos_data.save()

    def save_shtat_table_button(self):
        file_name = self.form.save_shtat_input.text()
        saver = Shtat_To_Excel(file_name)
        saver.shtat_to_excel()

    def count_button(self):
        main_data = Count_stimul_data(self)
        return main_data


if __name__ == '__main__':
    gui = Gui()
