import pandas as pd
import numpy as np
from darts import TimeSeries
from darts.models import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime as dt
from prophet import Prophet

path = '../datasets/'
def getData(croType):
  if croType=="BTC":
    ori_df = pd.read_csv(f"{path}{croType}/gemini_BTCUSD_2015_1min.csv")
    for item in range(2016, 2022):
      df = pd.read_csv(f"{path}{croType}/gemini_BTCUSD_{item}_1min.csv")
      new_df = pd.concat([ori_df, df], ignore_index=True)
      ori_df = new_df
    df = ori_df

  elif croType=="ETH":
    # Todo remove first line of CSV file
    ori_df = pd.read_csv(f"{path}{croType}/gemini_BTCUSD_2016_1min.csv")
    for item in range(2017, 2022):
      df = pd.read_csv(f"{path}/gemini_BTCUSD_{item}_1min.csv")
      new_df = pd.concat([ori_df, df], ignore_index=True)
      ori_df = new_df
    df = ori_df

  elif croType == "LTC":
    # Todo remove first line of CSV file
    ori_df = pd.read_csv(f"{path}{croType}/gemini_BTCUSD_2018_1min.csv")
    for item in range(2019, 2022):
      df = pd.read_csv(f"{path}/gemini_BTCUSD_{item}_1min.csv")
      new_df = pd.concat([ori_df, df], ignore_index=True)
      ori_df = new_df
    df = ori_df

  df.index = df.index[::-1]
  data = df.reindex(index=df.index[::-1])

  return data


### replace by get Data
data = getData("BTC")
data_close = data['Close']
data_close = data_close.values.reshape(len(data_close), 1)
data_date = [None] * len(data['Date'])
for index, i in enumerate(data['Date']):
  data_date[index] = i[6:10] + i[3:5] + i[0:2]
ticker_spacing = data_date
ticker_spacing = 90 # 3 month


#%%

# original data graph, (date close)

# Matplotlib example
# fig, ax = plt.subplots(1,1)
# ax.plot(data_date,data_close)
# ax.xaxis.set_major_locator(ticker.MultipleLocator(ticker_spacing))
# plt.rcParams["figure.figsize"] = (14,4)
# plt.xticks(rotation = 45)
# plt.title("BitCoin", fontsize=20)
# plt.show()

# TODO double check
# # statsmodels - seasonal_decompose
# # multiplicative Decomposition: yt = St x Tt x Et*
# forecast = seasonal_decompose(data['Close'].values, 'multiplicative', period=365)
# plt.rcParams.update({'figure.figsize': (15,15)})
# forecast.plot()
# plt.show()


# Darts
# data['Date'] = data_date
# series = TimeSeries.from_dataframe(data,'Date','Close')
# #train, val = series[:-365], series[-365:]
# train, val = series.split_before(len(data) - 365)
# model = ExponentialSmoothing()
# model.fit(train)
# prediction = model.predict(len(val))
# series.plot(label='actual')
# prediction.plot(label='forecast')
# plt.rcParams["figure.figsize"] = (14,4)
# plt.legend()
# plt.figure()
# plt.show()

# FBprophet
#TODO
# 1. apply the csv with minutes,
# 2. think about the scale
# 3. list out the algorithm we use
# list out everything you need before apply the algorithm, i figure the dataformat and date to you
# @chiiong

df = getData("BTC")
# df = ("gemini_BTCUSD_day.csv", usecols = ['Date','Close'])
df.index = df.index[::-1]
df = df.reindex(index=df.index[::-1])
df_date = [None] * len(df['Date'])

# have easy way to do this
# restructure the timestamp dataframe 可以做，很简单的
for index, i in enumerate(df['Date']):
   df_date[index] = i[6:10] + '-'+ i[3:5] + '-' + i[0:2]
df['Date'] = df_date

df.rename(columns = {'Date':'ds', 'Close':'y' }, inplace = True)
df.head()
m = Prophet()
m.fit(df)
future = m.make_future_dataframe(periods = 365)
future.tail()
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
fig1 = m.plot(forecast)
fig2 = m.plot_components(forecast)


# next try - yearly_seasonality
model = Prophet(daily_seasonality = False, weekly_seasonality = False, yearly_seasonality = True, seasonality_mode = 'multiplicative', growth = 'linear')
model.fit(df)
future = model.make_future_dataframe(periods = 365)
forecast = model.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

fig1 = model.plot(forecast)

fig2 = model.plot_components(forecast)
