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
    This message was sent because somebody requested to confirm ownership of the following email address ({0}) on the webpage http://galgantar.tk.

    In order to complete the confirmation, follow the URL: {1}
    """.format(receiver_email, confirmation_link)

    html = """\
    <h1 style="color: black">Email confirmation</h1>

    <p style="color: black">This message was sent because somebody requested to confirm ownership of the following email address {0} on the webpage <a href='http://galgantar.tk'>galgantar.tk</a>.</p>
    <p style="color: black">In order to complete the confirmation, click the link below:</p>

    <a style="display: block; padding: 10px; background-color: #007bff; border-radius: 2px; font-size: 15px; width: max-content; text-decoration: none; color: white;" href='{1}'>Confirm email</a>

    <p>If link is not working follow the URL: {1}</p>

    <p style="color: black">Kind regards,</p>
    <p style="color: black">Gal</p>
    <p style="color: black">P.S. Če si moj sošolc ne sprašuj ampak sam klikn</p>
    """.format(receiver_email, confirmation_link)

    send_email(receiver_email, subject, text, html)

def send_password_reset(receiver_email, confirmation_link):
    subject = "Forgot password"

    text = """\
    This message was sent because somebody requested to change password for the following account({0}) on the webpage http://galgantar.tk.

    In order to reset your password follow the URL: {1}
            """.format(receiver_email, confirmation_link)

    html = """\
    <h1 style="color: black">Forgot password</h1>

    <p style="color: black">This message was sent because somebody requested to change password for the following account({0}) on the webpage <a href='http://galgantar.tk'>galgantar.tk</a>.</p>
    <p style="color: black">In order to reset your password, click the link below: </p>

    <a style="display: block; padding: 10px; background-color: #007bff; border-radius: 2px; font-size: 15px; width: max-content; text-decoration: none; color: white;" href='{1}'>Reset password</a>

    <p>If link is not working follow the URL: {1}</p>
    <p style="color: black">Kind regards,</p>
    <p style="color: black">Gal</p>
            """.format(receiver_email, confirmation_link)

    send_email(receiver_email, subject, text, html)

if __name__ == '__main__':
    send_conformation("gantar.gal@gmail.com", "http://test.com")
    print("Email sent!")
