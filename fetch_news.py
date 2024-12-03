import requests
import json
import os

# Replace with your NewsAPI key
NEWS_API_KEY = 'newsapikey'

def is_valid_url(url):
    """Check if the URL is reachable and valid."""
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def fetch_articles(query, language='en', page_size=5):
    """Fetches articles from NewsAPI based on a query."""
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': query,
        'language': language,
        'pageSize': page_size,
        'apiKey': NEWS_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()

        # Debugging: Print the full response
        print("Response from NewsAPI:", json.dumps(data, indent=4))

        if 'articles' in data:
            articles = data['articles']
            valid_articles = []
            
            # Validate each article
            for article in articles:
                title = article.get('title')
                content = article.get('content')
                url = article.get('url')

                # Check for missing fields and invalid URL
                if title and content and url and is_valid_url(url):
                    valid_articles.append(article)
                else:
                    # Debugging: Print details of the skipped article
                    print(f"Article skipped (missing fields or invalid URL): {article['title'] if 'title' in article else 'No title'}")
            
            return valid_articles
        else:
            print("No articles found in the response.")
            return []

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def save_articles_to_file(articles, filename='articles.json'):
    """Saves articles to a JSON file for later processing."""
    # Ensure the current directory is correct
    print("Current working directory:", os.getcwd())

    if not articles:
        print("No articles to save.")
        return
    
    try:
        with open(filename, 'w') as file:
            json.dump(articles, file, indent=4)
        print(f"Articles successfully saved to '{filename}'.")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    topic = input("What topic are you searching for? ")  # Change to any topic of interest
    articles = fetch_articles(topic)

    if articles:
        print(f"\nFetched {len(articles)} articles about '{topic}'.")
        save_articles_to_file(articles)
    else:
        print("No articles found.")