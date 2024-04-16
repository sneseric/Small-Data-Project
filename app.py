from flask import Flask, render_template
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Retrieve API key from environment variable
api_key = os.getenv('NEWS_API_KEY')

# Initialize News API client
api = NewsApiClient(api_key=api_key)

# Generate common plural forms of a keyword
def plural_forms(keyword):
    """Generate common plural forms of a keyword."""
    return [keyword + suffix for suffix in ['', 's', 'es', 'ies', 'ves']]

# Remove % display for categories with less than 1% of the total
def autopct_format(values):
    def my_format(pct):
        return ('%.1f%%' % pct) if pct > 1 else ''
    return my_format

@app.route('/')
def index():
    # Fetch headlines for Orlando, FL
    top_headlines = api.get_everything(
        q='(Orlando AND Florida) OR (Altamonte Springs AND Florida) OR (Orange County AND Florida)',
        language='en',
        sort_by='relevancy'   # Other sorting options: 'popularity', 'publishedAt'
    )

    # Count articles related to theme parks
    theme_park_keywords = ['Disney World', 'Universal Studios', 'SeaWorld', 'Orlando theme park', 'Orlando amusement park']
    theme_park_articles = [article for article in top_headlines['articles'] if any(keyword.lower() in article['title'].lower() or keyword.lower() in article['content'].lower() for keyword in theme_park_keywords)]

    # Count articles related to DeSantis
    desantis_keywords = ['Ron DeSantis', 'Desantis', 'Florida governor', 'Governor']
    desantis_articles = [article for article in top_headlines['articles'] if any(keyword.lower() in article['title'].lower() or keyword.lower() in article['content'].lower() for keyword in desantis_keywords)]

    # Updated sports-related articles count
    sports_keywords = ['football', 'basketball', 'baseball', 'soccer', 'tennis', 'golf', 'LeBron James', 'Lionel Messi',
                       'Serena Williams', 'Tom Brady', 'Tiger Woods', 'Travis Kelce']
    sports_articles = [article for article in top_headlines['articles'] if any(keyword.lower() in article['title'].lower() or keyword.lower() in article['content'].lower() for keyword in sports_keywords)]

    # Keywords for food/restaurants
    food_keywords = ['restaurant', 'food', 'dining', 'cuisine', 'eatery']
    food_articles = [article for article in top_headlines['articles'] if any(any(plural_form.lower() in article['title'].lower() or plural_form.lower() in article['content'].lower() for plural_form in plural_forms(keyword)) for keyword in food_keywords)]

    # Keywords for entertainment
    entertainment_keywords = ['entertainment', 'movie', 'concert', 'event', 'festival', 'theater', 'music', 'band']
    entertainment_articles = [article for article in top_headlines['articles'] if any(any(plural_form.lower() in article['title'].lower() or plural_form.lower() in article['content'].lower() for plural_form in plural_forms(keyword)) for keyword in entertainment_keywords)]

    # Keywords for schools
    school_keywords = ['University of Central Florida', 'UCF', 'Valencia College', 'Valencia', 'Seminole State College of Florida',
                       'Full Sail University', 'Full Sail', 'Rollins College', 'Rollins', 'Florida A&M University', 'FAMU']
    school_articles = [article for article in top_headlines['articles'] if any(keyword.lower() in article['title'].lower() or keyword.lower() in article['content'].lower() for keyword in school_keywords)]

    # Keywords for science and technology
    science_technology_keywords = ['NASA', 'Kennedy Space Center', 'space', 'science', 'research', 'laboratory',
                                   'experiment', 'technology', 'tech', 'innovation', 'startup', 'Silicon Valley South', 'simulation',
                                   'virtual reality', 'augmented reality', 'gaming', 'software', 'hardware', 'astronaut', 'artificial intelligence', 'ai', 'a.i.', 'Social Media', 'Facebook', 'Reddit']
    science_technology_articles = [article for article in top_headlines['articles'] if any(any(plural_form.lower() in article['title'].lower() or plural_form.lower() in article['content'].lower() for plural_form in plural_forms(keyword)) for keyword in science_technology_keywords)]

    # Count other articles
    other_articles = len(top_headlines['articles']) - len(theme_park_articles) - len(desantis_articles) - len(
        sports_articles) - len(food_articles) - len(entertainment_articles) - len(school_articles) - len(
        science_technology_articles)

    # DATA VISUALIZATION
    # Create pie chart for news categories
    plt.figure(figsize=(6, 6))
    categories = ['Theme Parks', 'DeSantis', 'Sports', 'Food', 'Entertainment', 'Education', 'Science and Tech',
                  'Other']
    articles_count = [len(theme_park_articles), len(desantis_articles), len(sports_articles), len(food_articles),
                      len(entertainment_articles), len(school_articles), len(science_technology_articles),
                      other_articles]

    # Create labels for categories with more than 1% of the total
    labels = [category if count / sum(articles_count) * 100 > 1 else '' for category, count in zip(categories, articles_count)]

    # Create the pie chart with autopct labels
    wedges, texts, autotexts = plt.pie(articles_count, labels=labels, autopct=autopct_format(articles_count))

    # For each autopct label (every third label), set the rotation to 'vertical'
    #for autotext in autotexts:
        #autotext.set_rotation('vertical')

    # For each autopct label, set the rotation to 'vertical' if the percentage is 5% or less
    for autotext in autotexts:
        try:
            pct = float(autotext.get_text().strip('%'))  # Get the percentage as a float
            if pct <= 5.0:  # Check if the percentage is 5% or less
                autotext.set_rotation('vertical')
        except ValueError:
            # Skip rotation if the label text cannot be converted to a float
            continue

    plt.title('Article Categories')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    pie_chart = base64.b64encode(buf.read()).decode('utf8')

    # Pass articles to template
    return render_template('index.html', articles=top_headlines['articles'], pie_chart=pie_chart)

if __name__ == '__main__':
    app.run(debug=True)