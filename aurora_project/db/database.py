import mysql.connector

# DB 연결
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234",
    database="aurora_project"
)

dbConnecter = mydb.cursor(dictionary=True)