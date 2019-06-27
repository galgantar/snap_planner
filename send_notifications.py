import mail
import database
import datetime

def send_notifications():
    connection = database.establish_connection()
    cursor = connection.cursor()

    time = datetime.datetime.now() + datetime.timedelta(days=2)
    time = time.strftime('%Y-%m-%d')

    cursor.execute("""\
                    SELECT Email, Parent FROM Dates
                    WHERE MainDate = %s
                    """, (time,))

    emails = cursor.fetchall()
    not_count = 0
    for email, parent in emails:
        mail.send_notification(email, parent)
        not_count += 1

    cursor.close()
    connection.close()

    print("{} Notifications send!".format(not_count))

send_notifications()
