# FinHealth

![Hackathon Award](https://img.shields.io/badge/Hackathon%20Best%20Use%20Of%20Streamlit-🏆-red)

## 🏆 Hackathon Achievement  
FinHealth won **Best Use of Streamlit out of 800+ participants** at **ConUHacks IX**, Québec's largest hackathon.

We employed Streamlit <img src="https://user-images.githubusercontent.com/7164864/217935870-c0bc60a3-6fc0-4047-b011-7b4c59488c91.png" alt="Streamlit logo" style="width:20px;"></img> to quickly build a web app that interacts with our **2 machine learning models**, and to display stock prices onto a candlestick chart 📈 All built in under **24 hours**! 🎉  The Devpost can be found here: https://devpost.com/software/budget-buddy-b42oin

---
## [🎥 Video Demo](https://youtu.be/KpJxbmD_Qhc)
<a href="https://youtu.be/KpJxbmD_Qhc">
  <img src="https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/003/255/626/datas/gallery.jpg" width="500">
</a>  

## 🚀 Inspiration  
We wanted to empower individuals to make informed financial decisions and better understand their investment strategies. Inspired by the complexity of stock data, ever-changing market news, and the challenges of personal financial planning, we built FinHealth to centralize these insights in a user-friendly platform.

---

## 🤷 What it does
- **Stock Recommendations**: A main dashboard showcasing stock charts, their news, recommended action (buy, sell, or hold) and sentiment (positive, neutral, or negative).
- **AI Chatbot**: Context-aware chat that factors in selected stock data and recent news for more informed conversations.
- **Personalized Analysis**: Users can submit their information and receive tailored investment advice and recommendations.
- **Portfolio Analysis**: An AI chatbot that analyzes screenshots of a user’s portfolio to offer deeper insights.

---

## 🛠️ Tech Stack  
- **Web app:** Streamlit / Python
- **Chatbot:** OpenAI API for question answering & personal recommendations
- **Sentiment Analysis:** NLTK
- **Buy/Sell/Hold Recommendation:** scikit-learn

---

## ⚔️ Challenges Faced  
- **Training the classification model** with good results was difficult, as we attempted various permutations of features to train on (ex: moving averages). Some permutations would give accuracies above 90% - as well as training the model on multiple stocks - but the predictions didn't make sense. At the end, we found **training one model for each stock** gave the best predictions.
- **Learning Streamlit**: Adapting to Streamlit’s unique structure and deployment model was a hurdle for our team.
- **AI Integration**: We discovered the importance of refining prompt engineering to ensure clear and context-aware recommendations.

---

## 🎯 Accomplishments  
✅ **Built a fully functional MVP** in **under 24 hours**, with **little to no sleep**.  
✅ Designed, implemented, and **iteratively improved** a **classification model to give good, accurate buy/sell/hold recommendations**.  
✅ Built a beautiful **candlestick chart UI** to display stock prices, using Streamlit  
✅ **Won Best Use of Streamlit out of 800+ participants** at **ConUHacks IX**!  

---

## 📚 What We Learned  
- Integrating **LLMs and Machine Learning Models into real-time applications** effectively.  
- Training **effective and accurate machine learning models**, while avoiding overfitting
- **Rapid Prototyping**: Streamlit allowed us to iterate quickly and incorporate user feedback on the fly.
- **AI Integration**: We discovered the importance of refining prompt engineering to ensure clear and context-aware recommendations.
