from db import database

dbConnecter = database.dbConnecter

# 조회
def getWebLinkList (): 
    sql = "SELECT * FROM webLink"

    dbConnecter.execute(sql)                      
    result = dbConnecter.fetchall() 
    
    return result

# 생성
def createWebLink (): 
    sql = "SELECT * FROM webLink"

    dbConnecter.execute(sql)                      
    result = dbConnecter.fetchall() 
    
    return result

# 수정
def updateWebLink (): 
    sql = "SELECT * FROM webLink"

    dbConnecter.execute(sql)                      
    result = dbConnecter.fetchall() 
    
    return result

# 삭제
def deleteWebLink (): 
    sql = "SELECT * FROM webLink"

    dbConnecter.execute(sql)                      
    result = dbConnecter.fetchall() 
    
    return result