import unittest
from main import Save_data
from window import Ui_MainWindow


class MyTestCase(unittest.TestCase):
    def test_save(self):
        Save_data()
        cur.execute("INSERT INTO salaries "
                    "(department_code, position, position_count, tarif, salary, fio)"
                    " VALUES ('33300', 'экономист', '1', '42700', '42700', 'Юрченко Станислав Дмитриевич');")
        cur.execute("SELECT department_code, position, position_count, tarif, salary, fio FROM salaries "
                    "WHERE fio = 'Юрченко Станислав Дмитриевич'")
        res = cur.fetchall()
        self.assertEqual(res[0][0], 33300)
        self.assertEqual(res[0][1], "экономист")
        self.assertEqual(res[0][2], 1)
        self.assertEqual(res[0][3], 42700)
        self.assertEqual(res[0][4], 42700)
        self.assertEqual(res[0][5], "Юрченко Станислав Дмитриевич")
        con.close()
        os.remove("shtat.db")