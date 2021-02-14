from connection import Connection


class Personel_summary:
    def __init__(self):
        self.con = Connection.connect()
        self.cur = self.con.cursor()
        self.code_list = []
        self.data = self.get_data()

    def get_data(self):
        self.cur.execute("SELECT * FROM salaries")
        return self.cur.fetchall()

    def get_department_dict(self):
        data_for_table = {}
        for string in self.data:
            if string[1] not in self.code_list:
                self.code_list.append(string[1])
        for i in self.code_list:
            data_for_table[i] = {"pp": {"sdelka": 0, "vremya": 0, "tech": 0, "summary": 0},
                                 "np": {"specialist": 0, "worker": 0, "summary": 0}}
        return data_for_table

    def data_counting(self):
        data_for_table = self.get_department_dict()
        for pos in self.data:
            if pos[6] != "Вакансия" and pos[7] != 1:
                if pos[10] == "sd":
                    data_for_table[pos[1]]["pp"]["sdelka"] += 1
                    data_for_table[pos[1]]["pp"]["summary"] += 1
                elif pos[10] == "ti":
                    data_for_table[pos[1]]["pp"]["vremya"] += 1
                    data_for_table[pos[1]]["pp"]["summary"] += 1
                elif pos[10] == "np" or pos[10] == "na":
                    data_for_table[pos[1]]["np"]["specialist"] += 1
                    data_for_table[pos[1]]["np"]["summary"] += 1
                elif pos[10] == "ws":
                    data_for_table[pos[1]]["np"]["worker"] += 1
                    data_for_table[pos[1]]["np"]["summary"] += 1
                elif pos[10] == "tt":
                    data_for_table[pos[1]]["pp"]["tech"] += 1       # TODO summary может подсчитываться формулами в форме
                    data_for_table[pos[1]]["pp"]["summary"] += 1
        return data_for_table


if __name__ == '__main__':
    pers = Personel_summary()
    data = pers.data_counting()

