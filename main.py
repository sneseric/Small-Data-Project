from flask import Flask, render_template
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import io
import base64

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
    #top_headlines = api.get_everything(q='Orlando + "Florida"', language='en', sort_by='relevancy')
    top_headlines = api.get_everything(
        q='(Orlando AND Florida) OR (Altamonte Springs AND Florida) OR (Orange County AND Florida)',
        language='en',
        #sort_by='relevancy'
        sort_by='publishedAt'
    )

    # Count articles related to theme parks
    theme_park_articles = sum(
        'Disney World' in article['title'] or 'Universal Studios' in article['title'] for article in
        top_headlines['articles'])
    other_articles = len(top_headlines['articles']) - theme_park_articles

    # Create pie chart
    plt.figure(figsize=(6, 6))
    plt.pie([theme_park_articles, other_articles], labels=['Theme Parks', 'Other'], autopct='%1.1f%%')
    plt.title('Article Categories')

    # Save pie chart to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Convert BytesIO object to base64 string
    pie_chart = base64.b64encode(buf.read()).decode('utf8')

    # Pass articles to template
    return render_template('index.html', articles=top_headlines['articles'], pie_chart=pie_chart)

if __name__ == '__main__':
    app.run(debug=True)
