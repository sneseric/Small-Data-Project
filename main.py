from flask import Flask, render_template
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Retrieve API key from environment variable
api_key = os.getenv('NEWS_API_KEY')

# Initialize News API client
api = NewsApiClient(api_key=api_key)

@app.route('/')
def index():
    # Fetch headlines for Orlando, FL
    top_headlines = api.get_everything(q='Orlando', language='en', sort_by='relevancy')

    # Pass articles to template
    return render_template('index.html', articles=top_headlines['articles'])

if __name__ == '__main__':
    app.run(debug=True)
