import mysql.connector
from datetime import datetime, timedelta
import random

def generate_mock_trends():
    """
    Generate realistic mock Google Trends data.
    Used because Google Trends API (pytrends) applies IP-level
    rate limiting that blocks automated requests.
    Data pattern mimics real AI keyword trends (2025 Q1-Q2).
    """
    print("Generating mock Google Trends data...")

    keywords = {
        "artificial intelligence": 85,   # base interest score
        "machine learning": 65,
        "ChatGPT": 75,
        "data science": 55,
        "large language model": 45
    }

    all_trends = []

    # Generate 13 weeks of data (3 months)
    start_date = datetime.today() - timedelta(weeks=13)

    for week_num in range(13):
        week_date = start_date + timedelta(weeks=week_num)
        week_str = week_date.strftime('%Y-%m-%d')

        for keyword, base_score in keywords.items():
            # Add small random variation (+/- 10) to make it look realistic
            variation = random.randint(-10, 10)
            score = max(0, min(100, base_score + variation))

            all_trends.append({
                "keyword": keyword,
                "week": week_str,
                "interest_score": score
            })

    print(f"Generated {len(all_trends)} trend data points")
    return all_trends


def save_trends_to_mysql(trends):
    connection = mysql.connector.connect(
        host="sakura.proxy.rlwy.net",
        port=47018,
        user="root",
        password="YArzqLLbeeBgwndxJHKcHYwaTGDFWmEF",
        database="railway"
    )
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_trends (
            id INT AUTO_INCREMENT PRIMARY KEY,
            keyword VARCHAR(100),
            week DATE,
            interest_score INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY unique_keyword_week (keyword, week)
        )
    """)

    saved = 0
    skipped = 0
    for trend in trends:
        try:
            cursor.execute("""
                INSERT IGNORE INTO ai_trends (keyword, week, interest_score)
                VALUES (%s, %s, %s)
            """, (trend["keyword"], trend["week"], trend["interest_score"]))
            if cursor.rowcount > 0:
                saved += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"Error saving trend: {e}")

    connection.commit()
    cursor.close()
    connection.close()
    print(f"Saved {saved} trend records | Skipped {skipped} duplicates")


if __name__ == "__main__":
    trends = generate_mock_trends()
    if trends:
        save_trends_to_mysql(trends)
    else:
        print("No trends data generated!")