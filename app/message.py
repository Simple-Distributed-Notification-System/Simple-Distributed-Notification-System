import smtplib
from email.message import EmailMessage
from app.config import EMAIL, EMAIL_PASSWORD, SERVER_URL

# The Page responsible for the verification email sent to the client when logging in

async def send_email(to_email, token):
    html_content = f"""
        <html>
            <body>
                <h1 style='color: green;'>Hello! {to_email.split("@")[0]}</h1>
                <p>Your token is: {SERVER_URL}/token/{to_email}/{token}</p>
            </body>
        </html>
    """
    
    # Create the email message
    message = EmailMessage()
    message['Subject'] = 'Email with HTML Template'
    message['From'] = EMAIL
    message['To'] = to_email

    message.add_alternative(html_content, subtype='html')

    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL, EMAIL_PASSWORD)
        smtp.send_message(message)

