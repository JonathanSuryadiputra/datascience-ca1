import pandas as pd


# get data to dataframe type
class Api:
    def __init__(self):
        self.year = None
        self.path = '../datasets/'


    def getData(self, year: int):
        if year is not None:
            self.year = year
        file_path = f"./file/gemini_BTCUSD_{self.year}_1min.csv"
        df = pd.read_csv(file_path, parse_dates=['Date'])
        df = df.sort_values('Date')
        return df

    def allData(self, croType):
        ori_df = pd.read_csv(f"{path}{croType}/gemini_BTCUSD_2015_1min.csv")
        for item in range(2016, 2022):
            df = pd.read_csv(f"{path}{croType}/gemini_BTCUSD_{item}_1min.csv")
            new_df = pd.concat([ori_df, df], ignore_index=True)
            data = new_df
        data.index = data.index[::-1]
        data = data.reindex(index=data.index[::-1])

        ori_df.rename({"Unix Timestamp": "Timestamp"}, axis=1, inplace=True)
        combine_df = ori_df
        combine_df.drop_duplicates(subset=["Timestamp"], keep='first', inplace=True)
        return combine_df