import unittest
from connection.connection import Connection
import os


class MyTestCase(unittest.TestCase):
    def test_database(self):
        con = Connection.connect()
        cur = con.cursor()
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


if __name__ == '__main__':
    unittest.main()
