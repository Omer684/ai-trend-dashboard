import requests
import mysql.connector
from textblob import TextBlob
from datetime import datetime

# NewsAPI.org - free, no verification needed
# Get key at: https://newsapi.org/register
NEWS_API_KEY = "YOUR_NEWSAPI_KEY_HERE"

def fetch_ai_news():
    print("Fetching AI news from NewsAPI...")
    
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "artificial intelligence OR machine learning OR ChatGPT OR LLM",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 50,
        "apiKey": "8cd5cc34b6d14c2f85a126b2873f03b5"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # DEBUG: print raw response status
        print(f"API Status: {data.get('status')}")
        
        if data.get("status") != "ok":
            print(f"API Error: {data.get('message', 'Unknown error')}")
            return []
        
        articles_raw = data.get("articles", [])
        print(f"Found {len(articles_raw)} articles")
        
        articles = []
        for item in articles_raw:
            if not isinstance(item, dict):
                print(f"Skipping non-dict item: {item}")
                continue
            
            title = item.get("title", "")
            description = item.get("description", "") or ""
            url_link = item.get("url", "")
            source = item.get("source", {}).get("name", "Unknown")
            published_at = item.get("publishedAt", "")[:10]  # YYYY-MM-DD
            
            if not title or title == "[Removed]":
                continue
            
            # Sentiment analysis
            text = f"{title} {description}"
            blob = TextBlob(text)
            sentiment_score = blob.sentiment.polarity  # -1 to 1
            
            if sentiment_score > 0.1:
                sentiment_label = "positive"
            elif sentiment_score < -0.1:
                sentiment_label = "negative"
            else:
                sentiment_label = "neutral"
            
            articles.append({
                "title": title[:500],
                "description": description[:1000],
                "url": url_link[:500],
                "source": source[:100],
                "published_at": published_at,
                "sentiment_score": round(sentiment_score, 4),
                "sentiment_label": sentiment_label
            })
        
        print(f"Processed {len(articles)} valid articles")
        return articles
    
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []


def save_news_to_mysql(articles):
    connection = mysql.connector.connect(
        host="sakura.proxy.rlwy.net",
        port=47018,
        user="root",
        password="YArzqLLbeeBgwndxJHKcHYwaTGDFWmEF",
        database="railway"
    )
    cursor = connection.cursor()
    
    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_news (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(500),
            description TEXT,
            url VARCHAR(500),
            source VARCHAR(100),
            published_at DATE,
            sentiment_score FLOAT,
            sentiment_label VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY unique_url (url(255))
        )
    """)
    
    saved = 0
    skipped = 0
    for article in articles:
        try:
            cursor.execute("""
                INSERT IGNORE INTO ai_news 
                (title, description, url, source, published_at, sentiment_score, sentiment_label)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                article["title"],
                article["description"],
                article["url"],
                article["source"],
                article["published_at"],
                article["sentiment_score"],
                article["sentiment_label"]
            ))
            if cursor.rowcount > 0:
                saved += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"Error saving article: {e}")
    
    connection.commit()
    cursor.close()
    connection.close()
    print(f"Saved {saved} new articles | Skipped {skipped} duplicates")


if __name__ == "__main__":
    articles = fetch_ai_news()
    if articles:
        save_news_to_mysql(articles)
    else:
        print("No news articles found!")