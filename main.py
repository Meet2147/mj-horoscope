from fastapi import FastAPI, HTTPException, Query
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

app = FastAPI()

def fetch_horoscope(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        horoscope_tag = soup.find(id='horo_content')
        if horoscope_tag:
            horoscope_text = horoscope_tag.get_text(strip=True)
            return horoscope_text
        else:
            return "Horoscope content not found."
    else:
        return "Failed to retrieve horoscope."

@app.get("/horoscope")
async def read_horoscope(sunsign: str = Query(..., description="The sunsign to fetch the horoscope for"),
                         time_period: str = Query(..., description="The time period for the horoscope (yesterday, today, tomorrow, weekly, monthly, yearly)")):
    base_url = "https://www.ganeshaspeaks.com/horoscopes/"
    
    # Mapping for dynamic URL parts
    url_mapping = {
        "yesterday": "yesterday-horoscope",
        "today": "daily-horoscope",
        "tomorrow": "tomorrow-horoscope",
        "weekly": "weekly-horoscope",
        "monthly": "monthly-horoscope",
        "yearly": "yearly-horoscope"
    }

    if time_period not in url_mapping:
        raise HTTPException(status_code=404, detail=f"Invalid time period. Choose from {list(url_mapping.keys())}.")

    # Construct the URL based on the time period
    url_part = url_mapping[time_period]
    url = f"{base_url}{url_part}/{sunsign.lower()}/"

    horoscope_text = fetch_horoscope(url)
    
    # For the date in the response, use the actual calendar date for yesterday, today, and tomorrow
    current_utc = datetime.now(timezone.utc)
    date_mapping = {
        "yesterday": (current_utc - timedelta(days=1)).strftime('%Y-%m-%d'),
        "today": current_utc.strftime('%Y-%m-%d'),
        "tomorrow": (current_utc + timedelta(days=1)).strftime('%Y-%m-%d')
    }

    return {
        "date": date_mapping.get(time_period, "Not applicable for weekly/monthly/yearly"),
        "sunsign": sunsign,
        "horoscope": horoscope_text
    }
