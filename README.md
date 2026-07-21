# AI Industry Intelligence Dashboard

A live analytics platform that tracks the AI job market, news sentiment, and search interest trends — then presents them in a polished, executive-style Streamlit dashboard.

**Stack:** Python · MySQL (Railway) · Streamlit · Plotly · TextBlob

---

## ⚙️ What It Does

| Module | Source | Output |
| :--- | :--- | :--- |
| `scraper.py` | RemoteOK API | Scrapes live AI/tech job postings (title, company, location, skills) into `ai_jobs` |
| `news_fetcher.py` | NewsAPI.org | Fetches AI news headlines, runs sentiment analysis (TextBlob), stores in `ai_news` |
| `trends_fetcher.py` | Generated | Produces realistic mock search-interest trends for key AI terms into `ai_trends` |
| `database.py` | MySQL | Creates and connects to the database/tables used by all other scripts |
| `dashboard.py` | All of the above | Executive-style Streamlit dashboard: KPI tiles, sentiment breakdown, hiring locations, keyword trends, latest news, in-demand skills |

## 🗂️ Project Structure

```text
ai_trend_dashboard/
├── database.py           # DB connection + table setup
├── scraper.py            # Job scraper (RemoteOK)
├── news_fetcher.py       # News fetcher + sentiment analysis
├── trends_fetcher.py     # Search-trend data generator
├── dashboard.py          # Streamlit dashboard (the product)
├── requirements.txt      # Python dependencies
└── README.md
