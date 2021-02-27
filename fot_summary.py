from connection import Connection
from get_outs import Read_Outs
from pprint import pprint


class FOT_summary:
    def __init__(self, fot, workdays, secret, stimul):
        self.conn = Connection.connect()
        self.fot = fot
        self.workdays = workdays
        self.secret = secret
        self.stimul = stimul
        self.data = self.get_shtat_data()
        self.code_list = []
        self.calculated = {}
        outs = Read_Outs("штатное.xlsx")
        self.outs_list = outs.loader()
        self.outs = {}
        for i in self.outs_list:
            self.outs[i[0]] = [i[4], i[5], i[6]]
        pprint(self.outs)

    def get_shtat_data(self):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM salaries WHERE (fio NOT LIKE '%Вакансия%') "
                       f"AND (position_type NOT LIKE '%na%')")
        return cursor.fetchall()

    def get_department_dict(self):
        for string in self.data:
            if string[1] not in self.calculated:
                self.code_list.append(string[1])
        for i in self.code_list:
            self.calculated[i] = {"pp": 0, "np": 0, "tt": 0, "summary": 0}

    def calculate_oklads(self):
        self.get_department_dict()
        self.real_salary_counting()
        for i in self.data:
            print(i)
            if i[10] == 'sd' or i[10] == 'ti':
                self.calculated[i[1]]["pp"] += i[5]
            elif i[10] == 'np' or i[10] == 'ws':
                self.calculated[i[1]]["np"] += i[5]
            else:
                self.calculated[i[1]]["tt"] += i[5]

    def calculate_percent(self):
        summa = 0
        for i, v in enumerate(self.calculated):
            summa += self.calculated[v]['pp']
            summa += self.calculated[v]['tt']
        fot_percent = self.fot / summa - 1
        print(summa)
        return fot_percent

    def real_salary_counting(self):
        for i in self.data:
            i = list(i)
            if i[7] == 1:
                salary = i[9]
            else:
                salary = i[5]
            try:
                print(salary)
                salary = salary / self.workdays * (self.workdays - self.outs[i[6]][0] - self.outs[i[6]][1] - self.outs[i[6]][2])
                self.data[i][5] = salary
                print(i[5])
            except:
                pass


if __name__ == '__main__':
    fot_counting = FOT_summary(54200000, 21, 150000, 1.5)
    fot_counting.calculate_oklads()
    res = fot_counting.calculate_percent()
    print(res)
