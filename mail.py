from jinja2 import Template

def send_email(receiver_email, subject, text, html):
    import smtplib, ssl
    import os
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    smtp_server = "smtp.gmail.com"
    port = 465
    password = os.environ["GMAIL_PASSWORD"]
    sender_email = os.environ["GMAIL_ADDRESS"]

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def send_conformation(receiver_email, confirmation_link):
    subject = "Email conformation"

    text = """\
    Somebody requested to confirm ownership of the following email address: {0} on the webpage galgantar.tk.

    In order to complete the confirmation, follow the URL: {1}
    """.format(receiver_email, confirmation_link)

    with open("static/emails/confirmation.html", "r") as f:
        html_template = Template(f.read())

    html = html_template.render(email=receiver_email, confirmation_link=confirmation_link)

    send_email(receiver_email, subject, text, html)

def send_password_reset(receiver_email, confirmation_link):
    subject = "Forgot password"

    text = """\
    Somebody requested to change password for the following account: {0} on the webpage galgantar.tk.

    In order to reset your password follow the URL: {1}
    """.format(receiver_email, confirmation_link)

    with open("static/emails/forgot_password.html", "r") as f:
        html_template = Template(f.read())

    html = html_template.render(email=receiver_email, confirmation_link=confirmation_link)

    send_email(receiver_email, subject, text, html)

if __name__ == '__main__':
    send_conformation("gantar.gal@gmail.com", "http://test.com")
    print("Email sent!")
