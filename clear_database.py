"""Used for deleting confirmations that have been unused for more that two days"""

import database
import datetime

connection = database.establish_connection()
cursor = connection.cursor()

time = datetime.datetime.utcnow() + datetime.timedelta(days=2)

formatted_time = time.strftime('%Y-%m-%d')

cursor.execute("""\
                DELETE FROM Confirmations
                WHERE Creation > %s;
                """, (formatted_time,))

cursor.close()
connection.commit()
connection.close()
