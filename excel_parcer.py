import pandas as pd
from connection import Connection
import settings


class shtat_excel_to_bd:
    def __init__(self):
        read = pd.read_excel(settings.parcing_file)
        self.res = read.values.tolist()

    def loader(self):
        con = Connection.connect()
        cur = con.cursor()
        for i in self.res:
            cur.execute(f"INSERT INTO salaries "
                        f"(department_code, position, position_count, "
                        f"tarif, salary, fio, decree, history, decree_tarif, position_type) "
                        f"VALUES ('{i[0]}', '{i[1]}', '{i[2]}', '{i[3]}', '{i[4]}', '{i[5]}', "
                        f"'{i[6]}', '{i[7]}', '{i[8]}', '{i[9]}');")
            con.commit()


if __name__ == '__main__':
    execute = shtat_excel_to_bd()
    execute.loader()

