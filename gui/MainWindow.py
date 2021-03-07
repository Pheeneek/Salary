import os
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication
from gui.save_data import Save_data
from gui.search import Search
from gui.actions import Count_stimul_data
from counting.shtat_to_excel import Shtat_To_Excel
from gui.Shtat_window import Shtat
from gui.actions import Actions
from connection import Connection
from counting.personel_to_excel import Personel_To_Excel


class Gui:
    """
    Класс отрисовки основного окна с двумя вкладками
    """

    def __init__(self):
        """
        Инициализация экземпляра класса
        """
        self.actions = Actions(self)
        months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль",
                  "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        departments = []
        con, cur = Connection.connect()
        cur.execute("SELECT DISTINCT department_code FROM salaries ORDER BY department_code;")
        for i in cur.fetchall():
            departments.append(str(i[0]))

        Form, Window = uic.loadUiType("gui/MainWindow.ui")

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
        self.form.count_button.clicked.connect(self.count_button)
        self.form.work_shtat_button.clicked.connect(self.work_shtat_button)
        self.form.right_button_max.clicked.connect(self.right_button_max)
        self.form.left_button_max.clicked.connect(self.left_button_max)
        self.form.file_button.clicked.connect(self.file_button)
        self.form.save_shtat_table_button.clicked.connect(self.save_shtat_table_button)
        self.form.save_stimul_table_button.clicked.connect(self.save_stimul_table_button)
        self.form.print_sheets_button.clicked.connect(self.print_sheets_button)
        self.form.save_personel_button.clicked.connect(self.save_personel_button)
        dirpath = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(dirpath, "folder.png")
        icon = QtGui.QIcon(icon_path)
        self.form.file_button.setIcon(icon)

        self.form.left_button.setEnabled(False)
        self.form.right_button.setEnabled(False)
        self.form.save_button.setEnabled(False)
        self.form.delete_button.setEnabled(False)
        self.form.left_button_max.setEnabled(False)
        self.form.right_button_max.setEnabled(False)
        self.form.right_button_max.setEnabled(False)

        self.form.month.addItems(months)
        self.form.department_input.addItems(departments)

        self.search = []
        self.current_position = 1
        app.exec()

    def save_personel_button(self):
        file = QtWidgets.QFileDialog.getSaveFileName()[0]
        if file.endswith(".xlsx") or file.endswith(".xls"):
            saver = Personel_To_Excel(file, self)
        else:
            saver = Personel_To_Excel(f"{file}.xlsx", self)
        saver.personel_to_excel()

    def file_button(self):
        """
        Метод кнопки выбора файла отклонений. Открывает диалог выбора файла,
        записывает результат выбора в поле file_input
        :return: None
        """
        get_file = QtWidgets.QFileDialog.getOpenFileName()[0]
        self.form.file_input.setText(get_file)

    def search_button(self):
        """
        Метод кнопки поиска. Создает экземпляр класcа Search и вызывает метод класса
        search_clicked
        :return: None
        """
        search_result = Search(self)
        self.search = search_result.search_clicked()

    def clear_button(self):
        """
        Метод кнопки очистки форм.
        :return: None
        """
        self.actions.clear_form()

    def right_button(self):
        """
        Метод кнопки "выбрать следующую позицию"
        :return: None
        """
        self.form.left_button.setEnabled(True)
        self.form.left_button_max.setEnabled(True)
        self.current_position += 1
        self.form.search_number.setText(f"Позиция : {self.current_position} из {len(self.search)}")
        if self.current_position >= len(self.search):
            self.form.right_button.setEnabled(False)
            self.form.right_button_max.setEnabled(False)
        self.actions.position_output(self.search[self.current_position - 1])

    def left_button(self):
        """
        Метод кнопки "Выбрать предыдущую позицию"
        :return: None
        """
        self.form.right_button.setEnabled(True)
        self.form.right_button_max.setEnabled(True)
        self.current_position -= 1
        self.form.search_number.setText(f"Позиция : {self.current_position} из {len(self.search)}")
        if self.current_position <= 1:
            self.form.left_button.setEnabled(False)
            self.form.left_button_max.setEnabled(False)
        self.actions.position_output(self.search[self.current_position - 1])

    def right_button_max(self):
        """
        Метод кнопки "Выбор последней позиции"
        :return: None
        """
        self.form.left_button_max.setEnabled(True)
        self.form.left_button.setEnabled(True)
        self.current_position = len(self.search)
        self.form.search_number.setText(f"Позиция : {self.current_position} из {len(self.search)}")
        self.form.right_button_max.setEnabled(False)
        self.form.right_button.setEnabled(False)
        self.actions.position_output(self.search[self.current_position - 1])

    def left_button_max(self):
        """
        Метод кнопки "Выбрать первое значение"
        :return: None
        """
        self.form.right_button_max.setEnabled(True)
        self.form.right_button.setEnabled(True)
        self.current_position = 1
        self.form.search_number.setText(f"Позиция : {self.current_position} из {len(self.search)}")
        self.form.left_button_max.setEnabled(False)
        self.form.left_button.setEnabled(False)
        self.actions.position_output(self.search[self.current_position - 1])

    def new_position_button(self):
        """
        Метод кнопки "Новая позиция". Очищает форму для заполнения, делает дотупной кнопку
        "Сохранить изменения"
        :return: None
        """
        self.actions.clear_form()
        self.form.save_button.setEnabled(True)

    def delete_button(self):
        """
        Метод кнопки "Удалить позицию". Запускает метод класса Actions delete_confirmation
        :return: None
        """
        self.actions.delete_confirmation()

    def save_button(self):
        """
        Метод кнопки "Сохранить изменения". Создает экземпляр класса Save_data, вызывает
        метод save класса
        :return: None
        """
        pos_data = Save_data(self)
        pos_data.save()

    @staticmethod
    def save_shtat_table_button():
        """
        Метод кнопки "Выгрузить для расчета отклонений". Считывает имя файла и сохраняет
        данные текущего штатного расписания в формате Excel для заполнения отклонений.
        :return: None
        """
        file = QtWidgets.QFileDialog.getSaveFileName()[0]
        saver = Shtat_To_Excel(f"{file}.xlsx")
        saver.shtat_to_excel()

    def count_button(self):
        """
        Метод кнопки "Рассчитать". Создает экземпляр класса Count_stimul_data
        :return: None
        """
        file = self.form.file_input.text()
        if file:
            Count_stimul_data(self, file)
        else:
            self.form.message_label.setText("Не выбран файл отклонений!")

    def work_shtat_button(self):
        """
        Метод кнопки "Работа со штатным расписанием". Открывает новое окно
        со штатным расписанием в табличном виде
        :return:
        """
        Work_shtat = Shtat(self.window)
        Work_shtat.show()

    def save_stimul_table_button(self):
        pass  # TODO Сделать выгрузку

    def print_sheets_button(self):
        pass  # TODO Сделать печать
