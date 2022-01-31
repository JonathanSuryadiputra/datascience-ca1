# coding a common def method
def dataClean(df):
    df.index = df.index[::-1]
    data = df.reindex(index=df.index[::-1])
    data_close = data['Close']
    data_close = data_close.values.reshape(len(data_close), 1)
    data_date = [None] * len(data['Date'])
    for index, i in enumerate(data['Date']):
        data_date[index] = i[6:10] + i[3:5] + i[0:2]
    return df
