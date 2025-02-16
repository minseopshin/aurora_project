from db import database

dbConnecter = database.dbConnecter

# 조회
def getUserList (userid): 
    print(userid)
    sql = "SELECT * FROM user WHERE userId = %s"
    data = (userid,)
    
    dbConnecter.execute(sql,data)                      
    result = dbConnecter.fetchall() 
    
    return result

# 생성
def createUser (userId, password): 
    sql = "INSERT INTO user (userId, password) VALUES (%s,%s)"
    data = (userId, password)
    
    dbConnecter.execute(sql, data)                      
    result = database.mydb.commit()
    
    return result
