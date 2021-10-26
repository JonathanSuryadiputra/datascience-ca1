import pandas as pd


# get data to dataframe type
class Api:
    def __init__(self):
        self.year = None


    def getData(self, year: int):
        if year is not None:
            self.year = year
        file_path = f"./file/gemini_BTCUSD_{self.year}_1min.csv"
        df = pd.read_csv(file_path, parse_dates=['Date'])
        df = df.sort_values('Date')
        return df
