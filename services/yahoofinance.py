import yfinance as yf
import pandas as pd

class YahooFinance:
    def get_stock_data(self, symbol: str, start: str, end: str) -> pd.DataFrame:
        stock = yf.Ticker(symbol)
        df = stock.history(start=start, end=end)
        return df

