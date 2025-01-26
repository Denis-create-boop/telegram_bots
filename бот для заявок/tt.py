import mysql.connector
from datetime import datetime

SECRET_KEY = "LiZa04031994"

db = mysql.connector.connect(
    host="localhost",
    database="BotBase",
    user="root",
    password=SECRET_KEY,
    use_pure=True,
)
cursor = db.cursor()

query = """SELECT * FROM applications WHERE MONTH(дата) = 5"""
num = 5
l = ()
cursor.execute(query)
for row in cursor:
    print(row)
