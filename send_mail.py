import os
import smtplib


# Function to send an email
def send_email():
    # SMTP server configuration and authentication information
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = os.environ.get('SMTP_USERNAME')
    smtp_password = os.environ.get('SMTP_PASSWORD')

    # Sender and recipient information
    sender_email = os.environ.get('SENDER_EMAIL')
    recipient_email = os.environ.get('RECIPIENT_EMAIL')

    # Add link to GitHub secrets of the repository
    repo_name = os.environ.get('REPO_NAME')
    github_secrets_url = f"https://github.com/{repo_name}/settings/secrets"

    # Message creation
    subject = '[APP Tweetlive] Token expiration notification'
    body = f"Your token will expire in less than 7 days. Please take necessary actions here: {github_secrets_url}."

    message = f'Subject: {subject}\n\n{body}'

    try:
        # SMTP server connexion 
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, message)
        print('E-mail sent successfully')

    except Exception as e:
        print(f'Error sending e-mail: {str(e)}')

    finally:
        # Close the connection to the SMTP server
        server.quit()