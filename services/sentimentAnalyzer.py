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
        
    def most_frequent(self, List):
        return max(set(List), key = List.count)
    
    def analyze_sentiment_from_json(self, json_data):
        list_results = []
        for news in json_data:
            content = news['content']
            summary = content['title'] + ' ' + content['description']
            sentiment = self.analyze_sentiment(summary)
            # negative and positive count for double to avoid too many neutral results
            if sentiment == 'Positive' or sentiment == 'Negative':
                list_results.extend([sentiment] * 2)
            else:
                list_results.append(sentiment)
        return self.most_frequent(list_results)
