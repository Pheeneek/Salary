from PyQt5.QtCore import Qt, QSortFilterProxyModel, QRect, QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import (QMainWindow,
                             QTableView)
from PyQt5 import QtWidgets
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
        self.shtat_table_view = QtWidgets.QTableView(self.centralwidget)
        self.shtat_table_view.setGeometry(QRect(0, 0, 1381, 821))
        self.shtat_table_view.setObjectName("shtat_table_view")
        self.shtat_table_view.resizeColumnsToContents()
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
        font = QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.filter_button.setFont(font)
        self.filter_button.setObjectName("filter_button")
        self.setCentralWidget(self.centralwidget)

        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("ShtatWindow", "Работа со штатным расписанием"))
        self.filter_label.setText(_translate("ShtatWindow", "Фильтровать по столбцу:"))
        self.filter_button.setText(_translate("ShtatWindow", "Поиск"))

        self.model = QSqlTableModel(self.shtat_table_view)
        self.model.setTable('salaries')
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setHeaderData(0, Qt.Horizontal, self.filters[0])
        self.model.setHeaderData(1, Qt.Horizontal, self.filters[1])
        self.model.setHeaderData(2, Qt.Horizontal, self.filters[2])
        self.model.setHeaderData(3, Qt.Horizontal, self.filters[3])
        self.model.setHeaderData(4, Qt.Horizontal, self.filters[4])
        self.model.setHeaderData(5, Qt.Horizontal, self.filters[5])
        self.model.setHeaderData(6, Qt.Horizontal, self.filters[6])
        self.model.setHeaderData(7, Qt.Horizontal, self.filters[7])
        self.model.setHeaderData(8, Qt.Horizontal, self.filters[8])
        self.model.setHeaderData(9, Qt.Horizontal, self.filters[9])
        self.model.setHeaderData(10, Qt.Horizontal, self.filters[10])
        self.model.select()

        self.view = QTableView(self.shtat_table_view)
        self.view.setGeometry(QRect(0, 0, 1381, 821))
        self.shtat_table_view.resizeColumnsToContents()
        self.view.resizeColumnsToContents()
        self.view.setSortingEnabled(True)

        self.proxyModelContact = QSortFilterProxyModel(self)
        self.proxyModelContact.setSourceModel(self.model)
        self.view.setModel(self.proxyModelContact)

        self.shtat_table_view.resizeColumnsToContents()
        self.filter_combo_box.addItems(self.filters)
        self.filter_button.clicked.connect(self.use_filter_button)

    def use_filter_button(self) -> None:
        """
        Функция кнопки "Поиск". Считывает паттерн из поля фильтра и применяет его к столбцу,
        выбранного в комбо-боксе фильтра
        :return: None
        """
        self.proxyModelContact.setFilterKeyColumn(self.filters.index(self.filter_combo_box.currentText()))
        self.proxyModelContact.setFilterRegExp(self.filter_input.text())
