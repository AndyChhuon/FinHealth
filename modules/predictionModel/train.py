import os
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

class StockPredictionModel:
    def __init__(self, ticker, threshold=0.02, days=90):
        self.ticker = ticker
        self.threshold = threshold
        self.days = days
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.encoder = LabelEncoder()
        self.features = [
            "Open", "High", "Low", "Close", "Volume", 
            "Percent Change (1D)", "Percent Change (1W)", 
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
    with open("files/company_tickers_sec.json") as f:
        company_tickers = json.load(f)
        random_companies = random.sample(list(company_tickers.values()), 30)

        accuracies = []
        model_filename = "stock_prediction_model.pkl"

        model = StockPredictionModel(ticker=random_companies[0])  # Initialize with first ticker if model not foud

        if os.path.exists(model_filename):
            model.load_model(model_filename)

        for ticker in random_companies:
            print(f"Analyzing {ticker}...")
            try:
                model.ticker = ticker
                hist_data = model.get_stock_data()
                hist_data = model.label_data(hist_data)
                X, y = model.prepare_data(hist_data)
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                model.train_model(X_train, y_train)
                accuracy = model.evaluate_model(X_test, y_test)
                print(f"Model Accuracy: {accuracy:.2f}")
                accuracies.append(accuracy)
            except Exception as e:
                print(f"Error: {ticker} not found")
                continue

        # Save the trained model
        model.save_model("stock_prediction_model.pkl")

        # Load the model and make a prediction
        model.load_model("stock_prediction_model.pkl")
        latest_data = yf.Ticker("WBA").history(period="200d")
        prediction = model.make_prediction(latest_data)
        print(f"Based on the current data, the recommendation is: {prediction}")

        # Plot the distribution of accuracies during training
        median_accuracy = np.median(accuracies)
        avg_accuracy = np.mean(accuracies)
        min_accuracy = np.min(accuracies)
        max_accuracy = np.max(accuracies)

        plt.figure(figsize=(10, 6))
        plt.hist(accuracies, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
        plt.title('Distribution of Model Accuracies for 30 Random Companies')
        plt.xlabel('Accuracy')
        plt.ylabel('Frequency')
        plt.grid(True, axis='y')
        
        stats_text = f'Median: {median_accuracy:.2f}\nAverage: {avg_accuracy:.2f}\nMin: {min_accuracy:.2f}\nMax: {max_accuracy:.2f}'
        plt.gca().text(0.95, 0.95, stats_text, transform=plt.gca().transAxes,
                    fontsize=12, verticalalignment='top', horizontalalignment='right', 
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
        
        plt.show()
