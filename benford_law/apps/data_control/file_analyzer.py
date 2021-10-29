import pandas as pd


class FileAnalyzer:

    def __init__(self, file):
        self.file = file
        self.df = None


    def readHeaders(self):
        try:
            self.df = pd.read_csv(self.file, sep=None)
            columns = self.df.columns.tolist()
            dataTypes = self.df.dtypes
            return columns, dataTypes
        except:
            return 'Error occured', 'Problem with reading data from file'


    def checkRequiredColumn(self, columns):
        if '7_2009' in columns:
            return True
        else:
            return False


    def findNumericColumns(self):
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        return self.df.select_dtypes(include=numerics).columns.tolist()


    def getRequiresDataSet(self, col_name):
        return self.df[[col_name]]
