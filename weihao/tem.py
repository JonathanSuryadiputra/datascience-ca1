import pandas as pd
path = '../datasets/'

def allData():
  ori_df = pd.read_csv(f"{path}gemini_BTCUSD_2015_1min.csv")
  for item in range(2016, 2022):
    df = pd.read_csv(f"{path}/gemini_BTCUSD_{item}_1min.csv")
    new_df = pd.concat([ori_df, df], ignore_index=True)
    ori_df = new_df

  ori_df.rename({"Unix Timestamp": "Timestamp"}, axis=1, inplace=True)
  combine_df = ori_df
  combine_df.drop_duplicates(subset=["Timestamp"], keep='first', inplace=True)

  return combine_df
if __name__ == '__main__':
  allData()
  breakpoint()
