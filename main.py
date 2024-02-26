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
    top_headlines = api.get_everything(
        q='(Orlando AND Florida) OR (Altamonte Springs AND Florida) OR (Orange County AND Florida)',
        language='en',
        sort_by='relevancy'   # Other sorting options: 'popularity', 'publishedAt'
    )

    # Count articles related to theme parks
    theme_park_articles = [article for article in top_headlines['articles'] if 'Disney World' in article['title'] or 'Universal Studios' in article['title']]

    # Count articles related to DeSantis
    desantis_articles = [article for article in top_headlines['articles'] if 'DeSantis' in article['title']]

    # Updated sports-related articles count
    sports_keywords = ['football', 'basketball', 'baseball', 'soccer', 'tennis', 'golf', 'LeBron James', 'Lionel Messi',
                       'Serena Williams', 'Tom Brady', 'Tiger Woods', 'Travis Kelce']
    sports_articles = [article for article in top_headlines['articles'] if
                       any(keyword in article['title'] for keyword in sports_keywords)]

    # Count other articles
    other_articles = len(top_headlines['articles']) - len(theme_park_articles) - len(desantis_articles) - len(
        sports_articles)

    # Create pie chart for news categories
    plt.figure(figsize=(6, 6))
    categories = ['Theme Parks', 'DeSantis', 'Sports', 'Other']
    articles_count = [len(theme_park_articles), len(desantis_articles), len(sports_articles), other_articles]
    plt.pie(articles_count, labels=categories, autopct='%1.1f%%')
    plt.title('Article Categories')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    pie_chart = base64.b64encode(buf.read()).decode('utf8')

    # Pass articles to template
    return render_template('index.html', articles=top_headlines['articles'], pie_chart=pie_chart)

if __name__ == '__main__':
    app.run(debug=True)