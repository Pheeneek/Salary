import unittest
import sqlite3


class MyTestCase(unittest.TestCase):
    def test_loader(self):
        con = sqlite3.connect('../shtat.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM salaries;")
        res = cur.fetchall()
        for i in res:
            print(i)
        con.close()


if __name__ == '__main__':
    unittest.main()
