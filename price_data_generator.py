import pandas as pd
import seaborn as sns
import requests
from datetime import datetime
import math


class DataGenerator:
    def __init__(self, interval, date_start, date_stop):
        self.interval = interval
        self.date_start = datetime.strptime(date_start, '%d/%m/%y').timestamp()*1000
        self.date_stop = datetime.strptime(date_stop, '%d/%m/%y').timestamp()*1000
        self.data = self.get_candlestick_data()

    def get_candlestick_data(self):
        df = pd.DataFrame(
            requests.get(self.get_url_with_parameters(self.date_start, self.offset_timestamp(self.date_start, 1))).json())
        for start, end in self.create_timestamp_data():
            df = df.append(pd.DataFrame(requests.get(self.get_url_with_parameters(start, end)).json()), ignore_index=True)\
                if end < self.date_stop else df.append(pd.DataFrame(requests.get(self.get_url_with_parameters(start, self.date_stop)).json()),
                                                       ignore_index=True)
        df.columns = ['open_tstmp', 'open', 'high', 'low', 'close', 'vol', 'close_tstmp', 'quote_vol', 'trades',
                      'taker_base', 'taker_quote', 'excess_column']
        return df

    def create_timestamp_data(self):
        return [[self.offset_timestamp(self.date_start, i+1), self.offset_timestamp(self.date_start, i+2)-1] for i in range(self.calculate_api_calls_number())]

    def calculate_api_calls_number(self):
        return math.ceil((self.date_stop - self.date_start)/(self.interval_to_ms()*500))

    def interval_to_ms(self):
        return int(self.interval[:-1])*60000 if self.interval[-1] == 'm' else int(self.interval[:-1])*3600000

    def offset_timestamp(self, start, times=0):
        return start + 500*self.interval_to_ms()*times

    def get_url_with_parameters(self, start, stop):
        return f"https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval={self.interval}&startTime={str(start)[:-2]}&endTime={str(stop)[:-2]}"

    def data_to_csv(self):
        self.data.to_csv(f'C:/Users/jzmuj/OneDrive/Pulpit/data_{self.date_start}_{self.interval}.csv')


if __name__ == '__main__':
    print(DataGenerator('1m', '01/10/21', '02/10/21').data_to_csv())