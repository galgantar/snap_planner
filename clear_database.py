import database

def deleteOldConfirmations():
    """Used for deleting confirmations that have been unused for more that two days"""
    import datetime

    connection = database.establish_connection()
    cursor = connection.cursor()

    time = datetime.datetime.utcnow() + datetime.timedelta(days=2)

    formatted_time = time.strftime('%Y-%m-%d')

    cursor.execute("""\
                    DELETE FROM Confirmations
                    WHERE Creation < %s;
                    """, (formatted_time,))

    cursor.close()
    connection.commit()
    connection.close()

    print("Old confirmations deleted!")

def deleteUnactiveDates():
    """Used for deleting dates marked as 'unactive' in the Dates table"""

    connection = database.establish_connection()
    cursor = connection.cursor()

    cursor.execute("""\
                    DELETE FROM Dates
                    WHERE Active = FALSE
                    """)
    cursor.close()
    connection.commit()
    connection.close()

    print("Unactive dates deleted!")

deleteOldConfirmations()
deleteUnactiveDates()

print("Database cleaned!")
