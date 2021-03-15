from PyQt5.QtCore import Qt, QSortFilterProxyModel, QRect, QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import (QMainWindow,
                             QTableView)
from PyQt5 import QtWidgets
from save_loads.full_shtat_to_excel import FullShtatToExcel
import settings


class Shtat(QMainWindow):
    """
    Класс, реализующий окно для работы со штатным расписанием в виде таблицы
    """
    con = QSqlDatabase.addDatabase('QSQLITE')
    con.setDatabaseName(settings.db_name)

    def __init__(self, parent: any = None) -> None:
        """
        Функция инициализации окна штатного расписания
        :param parent: Родительский виджет (окно)
        """
        super().__init__(parent)
        self.filters = ['Номер',
                        'Подразделение',
                        'Должность',
                        'Количество',
                        'Тариф',
                        'Оклад',
                        'ФИО',
                        'Декрет',
                        'История',
                        'Оклад замещающего работника',
                        'Вид позиции',
                        ]
        self.setObjectName("ShtatWindow")
        self.resize(1380, 886)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.view = QTableView(self.centralwidget)
        self.view.setGeometry(QRect(0, 0, 1381, 821))
        self.view.setObjectName("shtat_table_view")
        self.view.setSortingEnabled(True)

        self.filter_combo_box = QtWidgets.QComboBox(self.centralwidget)
        self.filter_combo_box.setGeometry(QRect(250, 840, 231, 31))
        self.filter_combo_box.setObjectName("filter_combo_box")
        self.filter_input = QtWidgets.QLineEdit(self.centralwidget)
        self.filter_input.setGeometry(QRect(500, 840, 281, 31))
        self.filter_input.setObjectName("filter_input")
        self.filter_label = QtWidgets.QLabel(self.centralwidget)
        self.filter_label.setGeometry(QRect(10, 840, 221, 31))
        font = QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.filter_label.setFont(font)
        self.filter_label.setObjectName("filter_label")
        self.filter_button = QtWidgets.QPushButton(self.centralwidget)
        self.filter_button.setGeometry(QRect(800, 840, 171, 31))
        self.save_shtat_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_shtat_button.setGeometry(QRect(1000, 840, 225, 31))
        self.filter_button.setFont(font)
        self.save_shtat_button.setFont(font)
        self.filter_button.setObjectName("filter_button")
        self.setCentralWidget(self.centralwidget)

        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("ShtatWindow", "Работа со штатным расписанием"))
        self.filter_label.setText(_translate("ShtatWindow", "Фильтровать по столбцу:"))
        self.filter_button.setText(_translate("ShtatWindow", "Поиск"))
        self.save_shtat_button.setText(_translate("ShtatWindow", "Выгрузить штатное расписание"))

        self.model = QSqlTableModel(self.view)
        self.model.setTable('salaries')
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        for i in range(0, len(self.filters)):
            self.model.setHeaderData(i, Qt.Horizontal, self.filters[i])
        self.model.select()

        self.proxyModelContact = QSortFilterProxyModel(self)
        self.proxyModelContact.setSourceModel(self.model)
        self.view.setModel(self.proxyModelContact)
        self.view.resizeColumnsToContents()
        self.filter_combo_box.addItems(self.filters)
        self.filter_button.clicked.connect(self.use_filter_button)
        self.save_shtat_button.clicked.connect(self.use_save_shtat_button)

    def use_filter_button(self) -> None:
        """
        Функция кнопки "Поиск". Считывает паттерн из поля фильтра и применяет его к столбцу,
        выбранного в комбо-боксе фильтра
        :return: None
        """
        self.proxyModelContact.setFilterKeyColumn(self.filters.index(self.filter_combo_box.currentText()))
        self.proxyModelContact.setFilterRegExp(self.filter_input.text())

    @staticmethod
    def use_save_shtat_button() -> None:
        """
        Функция кнопки "Выгрузить штатное расписание". Выгружает все штатное расписание в
        файл формата Excel
        :return: None
        """
        file = QtWidgets.QFileDialog.getSaveFileName()[0]
        saver = FullShtatToExcel(file if file.endswith(".xlsx") else f"{file}.xlsx")
        saver.full_shtat_to_excel()
