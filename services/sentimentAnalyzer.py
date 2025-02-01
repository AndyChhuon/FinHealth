import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    def __init__(self):
        self._ensure_vader_lexicon()
        self.sid = SentimentIntensityAnalyzer()
    
    def _ensure_vader_lexicon(self):
        try:
            nltk.data.find('sentiment/vader_lexicon.zip')
        except LookupError:
            nltk.download('vader_lexicon')
    
    def analyze_sentiment(self, text):
        score = self.sid.polarity_scores(text)
        if score['compound'] >= 0.05:
            return 'Positive'
        elif score['compound'] <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'
