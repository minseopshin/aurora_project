import mysql.connector
from config import dbConfig

# DB 연결
mydb = mysql.connector.connect(
    host=dbConfig.DB_HOST,
    user=dbConfig.DB_USER,
    passwd=dbConfig.DB_PASSWORD,
    database=dbConfig.DB_NAME
)

dbConnecter = mydb.cursor(dictionary=True)