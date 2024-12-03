import openai
import json

# Set your OpenAI API key
openai.api_key = "api key"

def summarize_article(title, content):
    """Summarizes a single article using OpenAI."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes articles."},
                {"role": "user", "content": f"Summarize this article in 2 sentences:\n\nTitle: {title}\n\nContent: {content}"}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error summarizing article: {e}"

def load_articles_from_file(filename='articles.json'):
    """Loads articles from a JSON file."""
    with open(filename, 'r') as file:
        data = json.load(file)
    
    # Debugging: Print the structure of the loaded data
    print("Loaded articles structure:", type(data), "\n", data)
    
    # Since the data is a list of articles, we return the list directly
    return data

if __name__ == "__main__":
    # Load articles from the file
    articles = load_articles_from_file()

    # Iterate and summarize
    for idx, article in enumerate(articles):
        # Debugging: Check the type of each article
        print(f"Processing article {idx + 1}: Type={type(article)}")

        # Ensure each article is a dictionary
        if isinstance(article, dict):
            title = article.get('title', 'No title')
            content = article.get('content', 'No content available')
            summary = summarize_article(title, content)
            print(f"\n{idx + 1}. {title}\n   {summary}\n")
        else:
            print(f"Skipping article {idx + 1} because it's not a dictionary.")