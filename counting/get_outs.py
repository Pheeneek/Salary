from pandas import read_excel


class Read_Outs:
    """
    Класс, считывающий данные отклонений из файла формата Excel
    """
    def __init__(self, file: str) -> None:
        """
        Метод инициализации класса, счтитывает файл Excel, переводит его в список
        :param file: файл для загрузки
        """
        read = read_excel(file)
        self.res = read.values.tolist()

    def loader(self) -> list:
        """
        Метод, возвращающий список с данными
        :return: self.res - список с данными отклонений
        """
        return self.res
