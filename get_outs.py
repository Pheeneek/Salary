import pandas as pd


class Read_Outs:
    def __init__(self, file):
        read = pd.read_excel(file)
        self.res = read.values.tolist()

    def loader(self):
        return self.res


if __name__ == '__main__':
    execute = Read_Outs("отклонения.xlsx")
    execute.loader()
