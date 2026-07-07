# 🚆 Trainlytics

Trainlytics is an intelligent train recommendation and delay prediction platform designed to help commuters choose the most reliable train based on historical performance data. The system analyzes train punctuality, arrival trends, and reliability metrics to recommend the best train for a selected destination and time window.

The platform combines data analytics with machine learning to estimate delays, predict expected arrival times, and provide actionable travel insights through an interactive Streamlit dashboard.

---
#### Link:- https://trainlytics-mihirpalatkar.streamlit.app/
---

## ✨ Features

### Smart Train Recommendation

* Recommends the most reliable train for a selected destination and arrival window.
* Ranks trains based on success rate and delay performance.

### Reliability Analytics

* Calculates train reliability using historical performance data.
* Provides reliability ratings such as Excellent, Good, Average, and Poor.

### Delay Prediction using Machine Learning

* Uses a Random Forest Regressor to predict train delays.
* Estimates expected arrival and departure times based on historical patterns.

### Alternative Train Suggestions

* Displays backup train options with typical arrival times.
* Shows success rate and average delay for each alternative.

### Interactive Dashboard

* Built with Streamlit for a modern and responsive user experience.
* Includes train rankings, performance metrics, and visual analytics.

---

## 🧠 Machine Learning Approach

Trainlytics uses a Random Forest Regression model trained on historical train data.

### Features Used

* Train Name
* Day of Week
* Destination

### Target Variable

* Arrival Delay (minutes)

### Output

* Predicted Delay
* Expected Arrival Time
* Reliability Assessment

---

## 📊 Dashboard Insights

The dashboard provides:

* Recommended Train
* Expected Departure Time
* Expected Arrival Time
* ML Predicted Delay
* Reliability Score
* Window Success Rate
* Alternative Trains
* Train Ranking Table
* Success Rate Comparison Chart

---

## 🛠️ Technology Stack

### Frontend

* Streamlit

### Data Processing

* Pandas
* OpenPyXL

### Machine Learning

* Scikit-Learn
* Random Forest Regressor
* Label Encoding

### Development Tools

* Python
* Jupyter Notebook
* Git & GitHub

---

## 📂 Project Structure

```text
Trainlytics
│
├── dashboard
│   └── app.py
│
├── data
│   └── train_data.xlsx
│
├── notebooks
│   └── trainlytics_eda.ipynb
│
├── src
│   ├── data_processor.py
│   ├── recommendation_engine.py
│   ├── ml_model.py
│   └── main.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Future Enhancements

* Real-time train tracking integration
* Larger training dataset
* Advanced prediction models
* Weather and seasonal impact analysis
* Deployment on Streamlit Cloud
* Mobile-friendly interface

---

## 👨‍💻 Author

**Mihir Palatkar**

B.Tech Information Technology Student

Passionate about Data Analytics, Machine Learning, and Full-Stack Development.
