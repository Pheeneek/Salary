from connection import Connection


class Change_Stimul:
    def __init__(self, data_list):
        self.data_list = data_list
        self.con, self.cur = Connection.connect()
        self.cur.execute("CREATE TABLE IF NOT EXISTS stimul_table "
                         "(department_code INT PRIMARY KEY NOT NULL, "
                         "pp_oklad DECIMAL(10) NOT NULL, "
                         "pp_stimul DECIMAL(10) NOT NULL, "
                         "np_oklad DECIMAL(10) NOT NULL, "
                         "np_stimul DECIMAL(10) NOT NULL, "
                         "tt_oklad DECIMAL(10) NOT NULL, "
                         "tt_stimul DECIMAL(10) NOT NULL, "
                         "fot_percent DECIMAL(10) NOT NULL);")
        self.cur.execute("DELETE FROM stimul_table;")
        for item in data_list:
            self.cur.execute(f"INSERT INTO stimul_table (department_code, pp_oklad, pp_stimul, "
                             f"np_oklad, np_stimul, tt_oklad, tt_stimul, fot_percent) "
                             f"VALUES('{item[0]}', '{item[1]}', '{item[2]}', '{item[3]}', "
                             f"'{item[4]}', '{item[5]}', '{item[6]}', '{item[7]}');")
        self.con.commit()

    #  TODO Доделать работу с формой вывода стимула
