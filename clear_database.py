import database
import datetime

def deleteOldConfirmations():
    """Used for deleting confirmations that have been unused for more than one day"""

    connection = database.establish_connection()
    cursor = connection.cursor()

    time = datetime.datetime.utcnow() + datetime.timedelta(days=1)

    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("""\
                    DELETE FROM Confirmations
                    WHERE Creation < %s OR Active = 'False';
                    """, (formatted_time,))

    cursor.close()
    connection.commit()
    connection.close()

    print("Old confirmations deleted!")

def deleteUnactiveDates():
    """Used for deleting dates marked as 'unactive' or expired in the Dates table"""

    connection = database.establish_connection()
    cursor = connection.cursor()

    time = datetime.datetime.utcnow()

    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("""\
                    DELETE FROM Dates
                    WHERE MainDate < %s OR Active = FALSE;
                    """, (formatted_time,))
    cursor.close()
    connection.commit()
    connection.close()

    print("Unactive dates deleted!")

deleteOldConfirmations()
deleteUnactiveDates()

print("Database cleaned!")
