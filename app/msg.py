import smtplib
from email.message import EmailMessage
from app.config import EMAIL, EMAIL_PASSWORD, SERVER_URL

async def send_email(to_email, token):
    # Format the HTML content with dynamic values
    html_content = f"""
        <html>
            <body>
                <h1 style='color: green;'>Hello! {to_email.split("@")[0]}</h1>
                <p>Your token is: {SERVER_URL}/token/{to_email}/{token}</p>
            </body>
        </html>
    """
    
    # Create the email message
    msg = EmailMessage()
    msg['Subject'] = 'Email with HTML Template'
    msg['From'] = EMAIL
    msg['To'] = to_email

    # Add plain text fallback and the HTML version
    msg.set_content("This is an HTML email. Please view it in an email client that supports HTML.")
    msg.add_alternative(html_content, subtype='html')

    # Send via Gmail SMTP
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print("✅ Email sent using external HTML file.")
