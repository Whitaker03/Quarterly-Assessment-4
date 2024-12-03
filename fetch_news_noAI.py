import requests
import streamlit as st
import yagmail
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# NewsAPI key and endpoint
news_api_key = "newapikey"  # Replace with your NewsAPI key
news_url = "https://newsapi.org/v2/everything"

# Streamlit app configuration
st.title("Daily News Platform with Emailing")

# Debugging: Indicate the script has started
st.write("Script started successfully!")

# User inputs
topic = st.text_input("Enter a topic to search for news", value="technology").strip()
recipient_email = st.text_input("Enter recipient email").strip()

# Fetch and Email News Button
if st.button("Fetch and Email News"):
    st.write("Button clicked! Fetching news...")

    # Fetch news articles
    params = {
        "q": topic,
        "apiKey": news_api_key,
        "language": "en",
        "pageSize": 5,  # Fetch up to 5 articles
        "sortBy": "publishedAt"
    }
    
    try:
        response = requests.get(news_url, params=params)
        response.raise_for_status()  # Raise error for HTTP issues
    except requests.RequestException as e:
        st.error(f"Error fetching news: {e}")
        st.stop()

    data = response.json()

    # Check if articles exist
    if "articles" in data and data["articles"]:
        articles = []

        # Display and collect news articles
        for article in data["articles"]:
            title = article.get("title", "No title available")
            description = article.get("description", "No description available")
            url = article.get("url", "#")
            image_url = article.get("urlToImage", None)

            st.subheader(title)
            if image_url:
                st.image(image_url)
            st.write(description)
            st.write(f"[Read more]({url})")
            st.markdown("---")

            # Collect article information for email content
            articles.append(f"**{title}**\n\n{description}\n\nRead more: {url}\n")

        # Combine articles into email content
        email_content = "\n\n".join(articles)

        # Send email
        if recipient_email:
            try:
                yag = yagmail.SMTP("samschooltech@gmail.com", "p4302214")  # Replace with your email credentials
                yag.send(
                    to=recipient_email,
                    subject=f"Daily News Summary on {topic.capitalize()}",
                    contents=email_content
                )
                st.success(f"News articles sent to {recipient_email}!")
            except Exception as e:
                st.error(f"Failed to send email: {e}")
    else:
        st.error("No articles found. Try a different topic.")
