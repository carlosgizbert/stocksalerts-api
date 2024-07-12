import os

from mailersend import emails

def send_email(subject, html_content, text_content, to_email):
    mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY', 'mlsn.10015acf4c50226829a05f5cad14fd710ad859d90bb1c18fa0fe2a98806e0dd4'))

    mail_body = {}

    mail_from = {
        "name": "Carlos Gizbert",
        "email": "no-reply@trial-3zxk54v087pgjy6v.mlsender.net",
    }

    recipients = [
        {
            "name": "Your Client",
            "email": to_email,
        }
    ]

    reply_to = {
        "name": "Name",
        "email": "reply@trial-3zxk54v087pgjy6v.mlsender.net",
    }

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject(subject, mail_body)
    mailer.set_html_content(html_content, mail_body)
    mailer.set_plaintext_content(text_content, mail_body)
    mailer.set_reply_to(reply_to, mail_body)

    response = mailer.send(mail_body)

    print(f"Email sent to {to_email}. Response: {response}")