"""
Файл с классом отрисовки основного окна и функциями кнопок
"""

import os
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication
from gui.save_data import SaveData
from gui.search import Search
from gui.Shtat_window import Shtat
from gui.actions import Actions
from counting.count_stimul_data import CountStimulData
from save_loads.shtat_to_excel import ShtatToExcel
from save_loads.personel_to_excel import PersonelToExcel
from save_loads.stumul_to_excel import StimulToExcel


class Gui:
    """
    Класс отрисовки основного окна с двумя вкладками
    """

    def __init__(self) -> None:
        """
        Инициализация экземпляра класса
        """
        self.actions = Actions(self)
        Form, Window = uic.loadUiType("gui/MainWindow.ui")

        app = QApplication([])
        self.window = Window()
        self.form = Form()
        self.form.setupUi(self.window)
        self.window.show()

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
        self.form.save_personel_button.clicked.connect(self.save_personel_button)
        self.form.clear_stimul.clicked.connect(self.clear_stimul_button)
        self.form.stimul_table.setColumnCount(8)
        self.form.stimul_table.setHorizontalHeaderLabels(['Подразделение', 'ПП оклады', 'ПП стимул',
                                                          'НП оклады', 'НП стимул',
                                                          'Технологи оклады', 'Технологи стимул', 'Процент'])
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
        self.form.save_stimul_table_button.setEnabled(False)

        self.search = []
        self.current_position = 1
        self.stimul_data = []
        app.exec()

    def save_personel_button(self) -> None:
        file = QtWidgets.QFileDialog.getSaveFileName()[0]
        if file.endswith(".xlsx") or file.endswith(".xls"):
            saver = PersonelToExcel(file, self)
        else:
            saver = PersonelToExcel(f"{file}.xlsx", self)
        saver.personel_to_excel()

    def file_button(self) -> None:
        """
        Метод кнопки выбора файла отклонений. Открывает диалог выбора файла,
        записывает результат выбора в поле file_input
        :return: None
        """
        get_file = QtWidgets.QFileDialog.getOpenFileName()[0]
        self.form.file_input.setText(get_file)

    def search_button(self) -> None:
        """
        Метод кнопки поиска. Создает экземпляр класcа Search и вызывает метод класса
        search_clicked
        :return: None
        """
        search_result = Search(self)
        self.search = search_result.search_clicked()

    def clear_button(self) -> None:
        """
        Метод кнопки очистки форм.
        :return: None
        """
        self.actions.clear_form()

    def right_button(self) -> None:
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

    def left_button(self) -> None:
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

    def right_button_max(self) -> None:
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

    def left_button_max(self) -> None:
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

    def new_position_button(self) -> None:
        """
        Метод кнопки "Новая позиция". Очищает форму для заполнения, делает дотупной кнопку
        "Сохранить изменения"
        :return: None
        """
        self.actions.clear_form()
        self.form.save_button.setEnabled(True)

    def delete_button(self) -> None:
        """
        Метод кнопки "Удалить позицию". Запускает метод класса Actions delete_confirmation
        :return: None
        """
        self.actions.delete_confirmation()

    def save_button(self) -> None:
        """
        Метод кнопки "Сохранить изменения". Создает экземпляр класса Save_data, вызывает
        метод save класса
        :return: None
        """
        pos_data = SaveData(self)
        pos_data.save()

    @staticmethod
    def save_shtat_table_button() -> None:
        """
        Метод кнопки "Выгрузить для расчета отклонений". Считывает имя файла и сохраняет
        данные текущего штатного расписания в формате Excel для заполнения отклонений.
        :return: None
        """
        file = QtWidgets.QFileDialog.getSaveFileName()[0]
        saver = ShtatToExcel(f"{file}.xlsx")
        saver.shtat_to_excel()

    def count_button(self) -> None:
        """
        Метод кнопки "Рассчитать". Создает экземпляр класса Count_stimul_data
        :return: None
        """
        file = self.form.file_input.text()
        if file:
            work_stimul_data = CountStimulData(self, file)
            try:
                summa = work_stimul_data.summa
                self.form.message_label.setText(f"Расчет произведен! Использовано ФОТ: {summa}!")
                self.form.save_stimul_table_button.setEnabled(True)
                self.stimul_data = work_stimul_data.data_list
            except AttributeError:
                pass
        else:
            self.form.message_label.setText("Не выбран файл отклонений!")

    def work_shtat_button(self) -> None:
        """
        Метод кнопки "Работа со штатным расписанием". Открывает новое окно
        со штатным расписанием в табличном виде
        :return: None
        """
        Work_shtat = Shtat(self.window)
        Work_shtat.show()

    def save_stimul_table_button(self) -> None:
        """
        Метод кнопки "Сохранить стимул". Считывает имя файла и сохраняет
        данные текущего расчета стимула в формате Excel для заполнения отклонений.
        :return: None
        """
        file = QtWidgets.QFileDialog.getSaveFileName()[0]
        saver = StimulToExcel(self, self.stimul_data, f"{file}.xlsx")
        saver.stimul_to_excel()

    def clear_stimul_button(self) -> None:
        """
        Метод кнопки очистки QTableWidget с данными расчета стимула
        :return: None
        """
        self.actions.clear_stimul_form()
