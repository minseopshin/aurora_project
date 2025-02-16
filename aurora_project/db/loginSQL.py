from db import database

dbConnecter = database.dbConnecter

# 조회
def getUserList (userid, pwd): 
    print(userid)
    sql = "SELECT * FROM user WHERE userId = %s and password = %s"
    data = (userid, pwd,)
    
    dbConnecter.execute(sql,data)                      
    result = dbConnecter.fetchall() 
    
    return result
