from connection.connection import Connection


class Search:
    """
    Класс, реализующий поиск
    """

    def __init__(self, qtgui: any) -> None:
        """
        Метод init класса
        :param qtgui: экземпляр класса TkGUI (отрисовки основного окна)
        """
        self.gui = qtgui
        self.search, self.current_position = [], 0
        self.con, self.cursor = Connection.connect()
        self.department = self.gui.form.department_input.currentText()
        self.position = self.gui.form.pos_input.text()
        self.fio = self.gui.form.fio_input.text()
        self.tarif = self.gui.form.tarif_input.text()
        self.salary = self.gui.form.salary_input.text()
        self.pos_count = self.gui.form.pos_count_input.text()
        try:
            self.cursor.execute(f"SELECT * FROM salaries WHERE "
                                f"(department_code LIKE '%{self.department}%') AND "
                                f"(position LIKE '%{self.position}%') AND "
                                f"(fio LIKE '%{self.fio}%') AND "
                                f"(tarif LIKE '%{self.tarif}%') AND "
                                f"(salary LIKE '%{self.salary}%') AND "
                                f"(position_count LIKE '%{self.pos_count}%');")
            self.search_result = self.cursor.fetchall()
        except NameError:
            pass

    def search_clicked(self) -> list:
        """
        Метод, обрабатывающий результат поиска, настраивает кнопки, выводит количество
        найденных позиций и выводит первое значение в формы окна.
        :return: self.result - список с результатами поиска, если он не пустой
        """
        if self.search_result and len(self.search_result) > 0:
            self.gui.form.search_number.setText(f"Позиция : {1} из {len(self.search_result)}")
            self.gui.form.delete_button.setEnabled(True)
            if len(self.search_result) > 1:
                self.gui.form.right_button.setEnabled(True)
                self.gui.form.right_button_max.setEnabled(True)
            else:
                self.gui.form.right_button.setEnabled(False)
                self.gui.form.right_button_max.setEnabled(False)
        else:
            self.gui.form.search_number.setText(f"Позиция : {0} из {0}")
        if self.search_result:
            self.gui.actions.position_output(self.search_result[0])
            return self.search_result
