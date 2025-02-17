from db import database

dbConnecter = database.dbConnecter

# 조회
def getWebLinkList (data): 
    sql = "SELECT * FROM webLink WHERE 1 = 1 AND delete_YN = 0"

    if data is not None:
        for key, value in data.items(): 
            if type(value) == int or type(value) == float:
                sql += f" AND {key} = {value}"
            elif key == "search" :
                sql += f" AND name like '%{value}%' "
            else :
                sql += f" AND {key} = '{value}'"

    print(sql)       
    dbConnecter.execute(sql)                      
    result = dbConnecter.fetchall() 

    
    return result

# 생성
def createWebLink (data): 

    sql = "INSERT INTO webLink (userNo,created_by,name,url,category,create_date) VALUES (%s,%s,%s,%s,%s,%s)"
    data = (data["userNo"], data["created_by"],data["name"], data["url"], data["category"],data["create_date"])
    
    dbConnecter.execute(sql, data)                      
    result = database.mydb.commit()
    
    return result

# 수정
def updateWebLink (webLinkNo,data): 
    sql = "UPDATE webLink SET"

    if data is not None:
        for key, value in data.items(): 
            if type(value) == int or type(value) == float:
                sql += f" {key} = {value},"
            else :
                sql += f" {key} = '{value}',"

    sql = sql[:-1] + f" WHERE webLinkNo = {webLinkNo}"

    print(sql)
    dbConnecter.execute(sql)                      
    result = database.mydb.commit()
    
    return result

# 삭제
def deleteWebLink (webLinkNo): 
    sql = "UPDATE webLink SET delete_YN = 1 WHERE webLinkNo=%s"
    data = (webLinkNo,)

    dbConnecter.execute(sql,data)                      
    result = database.mydb.commit()
    
    return result