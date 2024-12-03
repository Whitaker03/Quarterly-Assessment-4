import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json

# Email configuration
SENDER_EMAIL = "senderemail@gmail.com"  # Your email address
SENDER_PASSWORD = "sender_password"  # Your email password (Use app password if 2FA is enabled)
RECIPIENT_EMAIL = "recipient_email"  # Recipient email address

# Load the articles (assuming you have a 'articles.json' with articles and summaries)
def load_articles_from_file(filename='articles.json'):
    """Loads articles from a JSON file."""
    with open(filename, 'r') as file:
        return json.load(file)

# Format the email body (create a clear structure with a bulleted list of summaries)
def format_email_body(articles):
    """Formats the email body with the list of articles."""
    email_body = "<h1>Latest Articles</h1>\n"
    
    for idx, article in enumerate(articles):  # Directly iterate over the articles list
        title = article.get('title', 'No title')
        description = article.get('description', 'No description available')
        url = article.get('url', '#')
        
        email_body += f"""
        <h2>{idx + 1}. {title}</h2>
        <p>{description}</p>
        <a href="{url}">Read more</a><br><br>
        """
    
    return email_body

# Send email function
def send_email(subject, body):
    """Sends an email with the specified subject and body."""
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject

    # Attach the email body (formatted HTML)
    msg.attach(MIMEText(body, 'html'))

    # Connect to Gmail's SMTP server and send the email
    try:
        # Set up the server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Login with your credentials
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())  # Send the email

        print("Email sent successfully!")
    
    except Exception as e:
        print(f"Error sending email: {e}")

# Main function to load articles and send the email
if __name__ == "__main__":
    # Load articles from the file
    articles = load_articles_from_file('articles.json')
    
    # Format the email body
    email_body = format_email_body(articles)
    
    # Define the subject
    subject = "Today's News Summary"
    
    # Send the email
    send_email(subject, email_body)