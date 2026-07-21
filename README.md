# 🤖 AI Industry Intelligence Dashboard

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

</p>

> **A production-ready analytics platform that monitors the AI industry by combining live job market data, news sentiment analysis, and AI trend insights into one interactive executive dashboard.**

## 🌐 Live Demo

**https://ai-trend-dashboard.streamlit.app/**

---

## 📸 Dashboard Preview

> (https://i.ibb.co/1GqhmrYW/Screenshot-2026-07-21-203414.png)


---

# 🚀 Project Overview

The AI industry is evolving rapidly, making it difficult to track hiring demand, emerging skills, and industry sentiment from multiple sources.

This project solves that problem by building a complete data analytics pipeline that:

- Collects live AI job listings
- Analyzes AI news using sentiment analysis
- Tracks AI keyword popularity
- Stores structured data in MySQL
- Presents business insights through an interactive dashboard

The result is a centralized AI market intelligence platform that enables users to monitor industry trends in real time.

---

# ✨ Features

### 📊 Executive KPI Dashboard

Monitor key business metrics including:

- Total AI jobs tracked
- AI news articles analyzed
- Average sentiment score
- Positive news coverage

---

### 💼 AI Job Market Analytics

Analyze hiring demand across the AI industry.

Insights include:

- Top hiring locations
- Companies actively recruiting
- Most requested AI skills
- Total job openings

---

### 📰 AI News Intelligence

Automatically fetches the latest AI news and performs sentiment analysis using Natural Language Processing.

Each article includes:

- Source
- Publication date
- Sentiment label
- Sentiment score

---

### 📈 AI Trend Monitoring

Visualizes keyword popularity across multiple weeks.

Tracked technologies include:

- Artificial Intelligence
- Machine Learning
- ChatGPT
- Data Science
- Large Language Models

---

### 📉 Interactive Visualizations

Built using Plotly for responsive analytics.

Includes:

- Bar Charts
- Donut Charts
- Trend Lines
- KPI Cards
- Interactive Tables

---

# 🛠 Tech Stack

| Category | Technologies |
|-----------|--------------|
| Language | Python |
| Dashboard | Streamlit |
| Database | MySQL |
| Data Analysis | Pandas |
| Visualization | Plotly |
| API Integration | Requests |
| NLP | TextBlob |
| Deployment | Streamlit Cloud |
| Cloud Database | Railway MySQL |

---

# 🏗 Architecture

```
              RemoteOK API
                     │
                     ▼
          AI Job Data Pipeline
                     │
                     ▼
                MySQL Database
                     ▲
                     │
NewsAPI ───► Sentiment Analysis

                     ▲
                     │
      AI Trends Generator

                     │
                     ▼

      Streamlit Analytics Dashboard
```

---

# 📂 Project Structure

```
AI-Industry-Intelligence-Dashboard/

│── dashboard.py
│── scraper.py
│── news_fetcher.py
│── trends_fetcher.py
│── database.py
│── requirements.txt
│── README.md
```

---

# 📊 Dashboard Insights

The dashboard provides real-time insights such as:

- AI hiring demand by location
- Most requested AI skills
- Industry news sentiment
- Historical keyword trends
- Executive KPI summary
- Latest AI news feed

---

# 🚀 Getting Started

Clone the repository

```bash
git clone https://github.com/Omer684/ai-trend-dashboard.git

cd ai-trend-dashboard
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run dashboard.py
```

---

# 💡 Engineering Challenges

### Live Data Integration

Integrated multiple external APIs into a unified analytics platform.

### Sentiment Analysis

Applied NLP techniques using TextBlob to classify AI news as:

- Positive
- Neutral
- Negative

### Data Modeling

Designed relational MySQL tables for jobs, news, and trend data while preventing duplicate records.

### Interactive Analytics

Built responsive Plotly visualizations that allow users to explore hiring patterns and market trends.

---

# 🎯 Skills Demonstrated

- Data Analytics
- Data Engineering
- ETL Pipeline Development
- API Integration
- SQL & Database Design
- Dashboard Development
- Data Visualization
- Sentiment Analysis
- Python Programming
- Business Intelligence
- Streamlit Deployment
- Cloud Database Management

---

# 🔮 Future Enhancements

- Real Google Trends integration
- Salary analytics
- Company comparison dashboard
- AI-powered insight generation
- Predictive hiring analytics
- User authentication
- Export reports (PDF & Excel)

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Muhammad Omer**

- GitHub: https://github.com/Omer684
- LinkedIn: www.linkedin.com/in/muhammad-omer-b63814317
- Live Dashboard: https://ai-trend-dashboard.streamlit.app/

---

⭐ **If you found this project useful, consider giving it a star!**
