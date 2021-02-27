from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication
from connection import Connection
from fot_summary import FOT_summary
from shtat_to_excel import Shtat_To_Excel


class Search:
    def __init__(self):
        self.con = Connection.connect()
        self.department = form.department_input.currentText()
        self.position = form.pos_input.text()
        self.fio = form.fio_input.text()
        self.tarif = form.tarif_input.text()
        self.salary = form.salary_input.text()
        self.pos_count = form.pos_count_input.text()
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
            form.search_number.setText(f"Позиция : {1} из {len(self.search_result)}")
            form.delete_button.setEnabled(True)
            if len(self.search_result) > 1:
                form.right_button.setEnabled(True)
            else:
                form.right_button.setEnabled(False)
        else:
            form.search_number.setText(f"Позиция : {0} из {0}")
        if self.search_result:
            Actions.position_output(self.search_result[0])
            return self.search_result


class Actions:
    @staticmethod
    def set_save():
        form.save_button.setEnabled(True)

    @staticmethod
    def position_output(pos_info):
        form.department_input.setCurrentText(f'{pos_info[1]}')
        form.pos_input.setText(f'{pos_info[2]}')
        form.pos_count_input.setText(f'{pos_info[3]}')
        form.fio_input.setText(f'{pos_info[6]}')
        form.tarif_input.setText(f'{pos_info[4]}')
        form.salary_input.setText(f'{pos_info[5]}')
        if pos_info[8] != '0':
            form.history_text.setText(f'{pos_info[8]}')
        else:
            form.history_text.clear()
        if pos_info[10] == 'na':
            form.na.setChecked(True)
        elif pos_info[10] == 'tt':
            form.tt.setChecked(True)
        elif pos_info[10] == 'sd':
            form.sd.setChecked(True)
        elif pos_info[10] == 'ws':
            form.ws.setChecked(True)
        elif pos_info[10] == 'ti':
            form.ti.setChecked(True)
        else:
            form.np.setChecked(True)
        if pos_info[7] == 1:
            form.do_y_n.setChecked(True)
            form.do_salary_input.setText(f"{pos_info[8]}")
        else:
            form.do_y_n.setChecked(False)
            form.do_salary_input.clear()
        Actions.make_changes()

    @staticmethod
    def make_changes():
        pass

    @staticmethod
    def clear_form():
        global search, current_position
        search, current_position = [], 0
        form.department_input.setCurrentIndex(0)
        form.pos_input.clear()
        form.pos_count_input.clear()
        form.fio_input.clear()
        form.tarif_input.clear()
        form.salary_input.clear()
        form.do_y_n.setChecked(False)
        form.do_salary_input.clear()
        form.vacancy.setChecked(False)
        form.history_text.clear()
        form.search_number.setText(f"Позиция : {current_position} из {len(search)}")
        form.left_button.setEnabled(False)
        form.right_button.setEnabled(False)
        form.delete_button.setEnabled(False)
        form.save_button.setEnabled(False)

    @staticmethod
    def delete_confirmation():
        global search, current_position
        message = f'Вы уверены, что хотите удалить штатную единицу "{search[current_position - 1][2]}"?'
        reply = QtWidgets.QMessageBox.question(window, 'Удаление штатной единицы', message,
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            conn = Connection.connect()
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM salaries WHERE id = '{search[current_position - 1][0]}';")
            conn.commit()
            Actions.clear_form()


class Save_data:
    def __init__(self):
        self.con = Connection.connect()
        self.department = form.department_input.currentText()
        self.position = form.pos_input.text()
        self.fio = form.fio_input.text()
        self.tarif = form.tarif_input.text()
        self.salary = form.salary_input.text()
        self.pos_count = form.pos_count_input.text()
        self.history = form.history_text.toPlainText()
        if form.na.isChecked():
            self.position_type = 'na'
        elif form.ws.isChecked():
            self.position_type = 'ws'
        elif form.ti.isChecked():
            self.position_type = 'ti'
        elif form.ws.isChecked():
            self.position_type = 'ws'
        elif form.np.isChecked():
            self.position_type = 'np'
        else:
            self.position_type = 'tt'
        if form.do_y_n.isChecked():
            self.decree = 1
            self.decree_tarif = form.do_salary_input.text()
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
            form.save_button.setEnabled(False)
            Save_data.save_confirmation()
        except:
            print("Ошибка записи в базу!!!")

    @staticmethod
    def save_confirmation():
        msg = QtWidgets.QMessageBox(window)
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Позиция упешно добавлена в базу!")
        msg.setWindowTitle("Сохранение позиции")
        msg.exec()

    def verify_data(self):
        pass  # TODO Сделать проверку вводимых данных на валидность


class Buttons:
    @staticmethod
    def search_button():
        global search
        search_result = Search()
        search = search_result.search_clicked()

    @staticmethod
    def clear_button():
        Actions.clear_form()

    @staticmethod
    def right_button():
        global search, current_position
        form.left_button.setEnabled(True)
        current_position += 1
        form.search_number.setText(f"Позиция : {current_position} из {len(search)}")
        if current_position >= len(search):
            form.right_button.setEnabled(False)
        Actions.position_output(search[current_position - 1])

    @staticmethod
    def left_button():
        global search, current_position
        form.right_button.setEnabled(True)
        current_position -= 1
        form.search_number.setText(f"Позиция : {current_position} из {len(search)}")
        if current_position <= 1:
            form.left_button.setEnabled(False)
        Actions.position_output(search[current_position - 1])

    @staticmethod
    def new_position_button():
        Actions.clear_form()
        form.save_button.setEnabled(True)

    @staticmethod
    def delete_button():
        Actions.delete_confirmation()

    @staticmethod
    def save_button():
        pos_data = Save_data()
        pos_data.save()

    @staticmethod
    def save_shtat_table_button():
        file_name = form.save_shtat_input.text()
        saver = Shtat_To_Excel(file_name)
        saver.shtat_to_excel()
    # ------------ Основной код ----------------


if __name__ == '__main__':
    # глобальные переменные для поиска и перемотки

    search = []
    current_position = 1  # TODO избавиться от глобальных переменных
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
    window = Window()
    form = Form()
    form.setupUi(window)
    window.show()

    # Определение начальных состояний и действий кнопок

    form.search_button.clicked.connect(Buttons.search_button)
    form.clear_form_buton.clicked.connect(Buttons.clear_button)
    form.right_button.clicked.connect(Buttons.right_button)
    form.left_button.clicked.connect(Buttons.left_button)
    form.new_position_button.clicked.connect(Buttons.new_position_button)
    form.delete_button.clicked.connect(Buttons.delete_button)
    form.save_button.clicked.connect(Buttons.save_button)
    form.save_shtat_table.clicked.connect(Buttons.save_shtat_table_button)

    form.left_button.setEnabled(False)
    form.right_button.setEnabled(False)
    form.save_button.setEnabled(False)
    form.delete_button.setEnabled(False)
    form.cancel_button.setEnabled(False)

    form.month.addItems(months)
    form.department_input.addItems(departments)
    # Запуск цикла

    app.exec()
