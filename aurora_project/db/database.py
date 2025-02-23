import mysql.connector
from config import Config

# DB 연결
mydb = mysql.connector.connect(
    host=Config.DB_HOST,
    user=Config.DB_USER,
    passwd=Config.DB_PASSWORD,
    database=Config.DB_NAME
)

dbConnecter = mydb.cursor(dictionary=True)