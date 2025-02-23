from db import database

dbConnecter = database.dbConnecter

# 조회
def getUserList (data): 
    sql = "SELECT * FROM user WHERE 1 = 1"
    if data is not None:
        for key, value in data.items(): 
            if type(value) == int or type(value) == float:
                sql += f" AND {key} = {value}"
            elif key == "search" :
                sql += f" AND userId like '%{value}%' "
            else :
                sql += f" AND {key} = '{value}'"

    dbConnecter.execute(sql)                      
    result = dbConnecter.fetchall() 

    print(sql)
    
    return result

def getShareUserList (data): 
    sql = "SELECT * FROM user u left join webLinkShare wls on u.userNo = wls.shareUserNo WHERE 1 = 1"
    if data is not None:
        for key, value in data.items(): 
            if key == "search" :
                sql += f" AND userId like '%{value}%' "
            else :
                sql += f" AND ({key} = '{value}' OR {key} IS NULL)"

    dbConnecter.execute(sql)                      
    result = dbConnecter.fetchall() 

    print(sql)
    
    return result


# 생성
def createUser (userId, password): 
    sql = "INSERT INTO user (userId, password) VALUES (%s,%s)"
    data = (userId, password)
    
    dbConnecter.execute(sql, data)                      
    result = database.mydb.commit()

    print(sql)
    
    return result
