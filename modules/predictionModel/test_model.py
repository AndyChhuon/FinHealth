import random
import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import json
import matplotlib.pyplot as plt
import numpy as np
import joblib
import os

class StockPredictionModel:
    def __init__(self, ticker, threshold=0.02, days=90):
        self.ticker = ticker
        self.threshold = threshold
        self.days = days
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.encoder = LabelEncoder()
        self.features = [
            "Open", "High", "Low", "Close", "Volume", 
            "Percent Change (1D)", "Percent Change (1W)"
        ]

    def get_stock_data(self):
        stock = yf.Ticker(self.ticker)
        hist = stock.history(period='max')
        hist["Percent Change (1D)"] = hist["Close"].pct_change() * 100
        hist["Percent Change (1W)"] = hist["Close"].pct_change(periods=7) * 100
        
        # Moving Averages
        hist["SMA_50"] = hist["Close"].rolling(window=50).mean()
        hist["SMA_200"] = hist["Close"].rolling(window=200).mean()
        hist["EMA_50"] = hist["Close"].ewm(span=50, adjust=False).mean()
        hist["EMA_200"] = hist["Close"].ewm(span=200, adjust=False).mean()
        
        # MACD
        hist["MACD"] = hist["Close"].ewm(span=12, adjust=False).mean() - hist["Close"].ewm(span=26, adjust=False).mean()
        hist["MACD_Signal"] = hist["MACD"].ewm(span=9, adjust=False).mean()
        
        # Rate of Change (ROC)
        hist["ROC"] = hist["Close"].pct_change(periods=12) * 100
        # Bollinger Bands
        hist["Bollinger_Upper"] = hist["SMA_50"] + (hist["Close"].rolling(window=20).std() * 2)
        hist["Bollinger_Lower"] = hist["SMA_50"] - (hist["Close"].rolling(window=20).std() * 2)
        return hist.dropna()

    def label_data(self, df):
        df["future_price"] = df["Close"].shift(-self.days)
        df["return"] = ((df["future_price"] - df["Close"]) / df["Close"]) * 100
        df["label"] = df["return"].apply(
            lambda x: "Buy" if x > self.threshold else ("Sell" if x < -self.threshold else "Hold")
        )
        return df.dropna()

    def prepare_data(self, hist_data):
        X = hist_data[self.features]
        y = self.encoder.fit_transform(hist_data["label"])
        return X, y

    def train_model(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def evaluate_model(self, X_test, y_test):
        accuracy = self.model.score(X_test, y_test)
        return accuracy

    def make_prediction(self, latest_data):
        latest_data["Percent Change (1D)"] = latest_data["Close"].pct_change() * 100
        latest_data["Percent Change (1W)"] = latest_data["Close"].pct_change(periods=7) * 100
        latest_data["SMA_50"] = latest_data["Close"].rolling(window=50).mean()
        latest_data["SMA_200"] = latest_data["Close"].rolling(window=200).mean()
        latest_data["EMA_50"] = latest_data["Close"].ewm(span=50, adjust=False).mean()
        latest_data["EMA_200"] = latest_data["Close"].ewm(span=200, adjust=False).mean()
        latest_data["MACD"] = latest_data["Close"].ewm(span=12, adjust=False).mean() - latest_data["Close"].ewm(span=26, adjust=False).mean()
        latest_data["MACD_Signal"] = latest_data["MACD"].ewm(span=9, adjust=False).mean()
        latest_data["ROC"] = latest_data["Close"].pct_change(periods=12) * 100
        latest_data["Bollinger_Upper"] = latest_data["SMA_50"] + (latest_data["Close"].rolling(window=20).std() * 2)
        latest_data["Bollinger_Lower"] = latest_data["SMA_50"] - (latest_data["Close"].rolling(window=20).std() * 2)
        latest_features = latest_data.tail(1)[self.features]
        prediction = self.model.predict(latest_features)
        return ["Buy", "Hold", "Sell"][prediction[0]]

    def save_model(self, filename):
        joblib.dump(self.model, filename)

    def load_model(self, filename):
        self.model = joblib.load(filename)

if __name__ == "__main__":
    model_filename = "stock_prediction_model.pkl"
    if os.path.exists(model_filename):
        # Load the model if it exists
        model = StockPredictionModel(ticker="WBA")  # Initialize with a default ticker
        model.load_model(model_filename)
        print("Model loaded from file.")

        # Load the model and make a prediction
        tickers = ["AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "NVDA", "JPM", "JNJ", "WMT", "DECK","WBA"]
        for ticker in tickers:
            print(f"Making prediction for {ticker}")
            latest_data = yf.Ticker(ticker).history(period="200d")
            prediction = model.make_prediction(latest_data)
            print(f"Based on the current data, the recommendation is: {prediction}")
    else:
        print("Model not found. Please train the model first.")
