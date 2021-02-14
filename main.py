from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication
from connection import Connection


class Search:
    def __init__(self):
        self.con = Connection.connect()
        self.department = form.dep_input.text()
        self.position = form.pos_input.text()
        self.fio = form.fio_input.text()
        self.tarif = form.tarif_input.text()
        self.salary = form.salary_input.text()
        self.pos_count = form.pos_count_input.text()
        cur = self.con.cursor()
        try:
            cur.execute(f"SELECT * FROM salaries WHERE "
                        f"(department_code LIKE '%{self.department}%') AND "
                        f"(position LIKE '%{self.position}%') AND "
                        f"(fio LIKE '%{self.fio}%') AND "
                        f"(tarif LIKE '%{self.tarif}%') AND "
                        f"(salary LIKE '%{self.salary}%') AND "
                        f"(position_count LIKE '%{self.pos_count}%');")
            self.search_result = cur.fetchall()
        except:
            pass

    def search_clicked(self):
        if self.search_result and len(self.search_result) > 0:
            form.search_number.setText(f"Позиция : {1} из {len(self.search_result)}")
            if len(self.search_result) > 1:
                form.right_button.setEnabled(True)
                form.delete_button.setEnabled(True)
        else:
            form.search_number.setText(f"Позиция : {0} из {0}")
        if self.search_result:
            Actions.position_output(self.search_result[0])
            return self.search_result


class Actions:
    @staticmethod
    def position_output(pos_info):
        print(pos_info)
        form.dep_input.setText(f'{pos_info[1]}')
        form.pos_input.setText(f'{pos_info[2]}')
        form.pos_count_input.setText(f'{pos_info[3]}')
        form.fio_input.setText(f'{pos_info[6]}')
        form.tarif_input.setText(f'{pos_info[4]}')
        form.salary_input.setText(f'{pos_info[5]}')
        if pos_info[8] != '0':
            form.history_text.setText(f'{pos_info[8]}')
        if pos_info[10] == 'na':
            form.na.setChecked(True)
        elif pos_info[10] == 'tt':
            form.tt.setChecked(True)
        elif pos_info[10] == 'sd' or pos_info[10] == 'ti':
            form.pp.setChecked(True)
        elif pos_info[10] == 'ws':
            form.ws.setChecked(True)
        else:
            form.np.setChecked(True)
        if pos_info[7] == 1:
            form.do_y_n.setChecked(True)
            form.do_salaty_input.setText(f"{pos_info[8]}")

    @staticmethod
    def clear_form():
        global search, current_position
        search, current_position = [], 0
        form.dep_input.clear()
        form.pos_input.clear()
        form.pos_count_input.clear()
        form.fio_input.clear()
        form.tarif_input.clear()
        form.salary_input.clear()
        form.do_y_n.setChecked(False)
        form.do_salaty_input.clear()
        form.vacancy.setChecked(False)
        form.search_number.setText(f"Позиция : {current_position} из {len(search)}")
        form.left_button.setEnabled(False)
        form.right_button.setEnabled(False)
        form.delete_button.setEnabled(False)

    @staticmethod
    def example():
        global search, current_position
        message = f'Вы уверены, что хотите удалить штатную единицу "{search[current_position - 1][2]}"?'
        reply = QtWidgets.QMessageBox.question(window, 'Удаление штатной единицы', message,
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:

            con = Connection.connect()
            cur = con.cursor()
            cur.execute(f"DELETE FROM salaries WHERE id = '{search[current_position - 1][0]}';")
            con.commit()
        else:
            print('cancel')


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
        Actions.example()
        Actions.clear_form()
    # ------------ Основной код ----------------


if __name__ == '__main__':
    # глобальные переменные для поиска и перемотки

    search = []
    current_position = 1

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

    form.left_button.setEnabled(False)
    form.right_button.setEnabled(False)
    form.save_button.setEnabled(False)
    form.delete_button.setEnabled(False)

    # Запуск цикла

    app.exec()
