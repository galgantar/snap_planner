import mail
import database
import datetime

def send_notifications():
    connection = database.establish_connection()
    cursor = connection.cursor()

    start_time = datetime.datetime.now() + datetime.timedelta(days=1)
    start_time = start_time.strftime('%Y-%m-%d') + " 23:59:59"

    end_time = datetime.datetime.now() + datetime.timedelta(days=3)
    end_time = end_time.strftime('%Y-%m-%d') + " 00:00:00"

    cursor.execute("""\
                    SELECT Email, Parent FROM Dates
                    WHERE MainDate BETWEEN %s AND %s
                    """, (start_time, end_time))

    emails = cursor.fetchall()
    not_count = 0
    for email, parent in emails:
        mail.send_notification(email, parent)
        not_count += 1

    cursor.close()
    connection.close()

    print("{} Notifications send!".format(not_count))

send_notifications()
