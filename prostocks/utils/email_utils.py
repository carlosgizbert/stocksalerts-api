import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(subject, body, to_email):
    message = Mail(
        from_email='carlosaugustogizbert@gmail.com',
        to_emails=to_email,
        subject=subject,
        html_content=body
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(f"Email sent to {to_email}. Status code: {response.status_code}")
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}. Error: {str(e)}")
        return False
