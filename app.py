from flask import Flask, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("NEWSAPI_KEY")
BASE_URL = os.getenv("NEWSAPI_BASE_URL", "https://newsapi.org/v2/top-headlines")

if not API_KEY:
    raise RuntimeError("NEWSAPI_KEY is not set. Add it to .env locally or set it in Render.")


@app.route("/")
@app.route("/<category>")
def home(category="general"):
    countries = ["us", "in"]  
    news = []

    for country in countries:
        url = f"{BASE_URL}?country={country}&category={category}&apiKey={API_KEY}"
        r = requests.get(url).json()
        print(f"DEBUG -> {category.upper()} ({country}) | status: {r.get('status')}, total: {r.get('totalResults')}, error: {r.get('message')}")
        
        news = r.get("articles", [])
        if news: 
            break

    categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]

    return render_template("home.html", allNews=news, active_category=category, categories=categories)


if __name__ == "__main__":
    app.run(debug=True)

