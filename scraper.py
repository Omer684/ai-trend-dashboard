import requests
from database import get_connection

def scrape_ai_jobs():
    print("Fetching AI jobs from RemoteOK...")

    url = "https://remoteok.com/api"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    data = response.json()

    all_jobs = []
    if not isinstance(data, list):
        print("Unexpected data format!")
        return []
    print(f"Total jobs available: {len(data)}")
    for job in data:
        if isinstance(job, dict) and "position" in job:
            all_jobs.append({
                "title": job.get("position", ""),
                "company": job.get("company", ""),
                "location": job.get("location", "Remote"),
                "skills": ", ".join(job.get("tags", []))
            })

    print(f"Scraped {len(all_jobs)} jobs!")
    return all_jobs

def save_jobs_to_mysql(jobs):
    connection = get_connection()
    cursor = connection.cursor()
    for job in jobs:
        cursor.execute("""
            INSERT INTO ai_jobs (title, company, location, skills)
            VALUES (%s, %s, %s, %s)
        """, (job["title"], job["company"], job["location"], job["skills"]))
    connection.commit()
    cursor.close()
    connection.close()
    print(f"Saved {len(jobs)} jobs to MySQL!")

if __name__ == "__main__":
    jobs = scrape_ai_jobs()
    if jobs:
        save_jobs_to_mysql(jobs)
    else:
        print("No jobs found!")