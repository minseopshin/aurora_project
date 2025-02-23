from db import database

dbConnecter = database.dbConnecter

# 조회
def getUserList (data): 
    sql = "SELECT * FROM user WHERE 1=1"
    if data is not None:
        for key, value in data.items(): 
            if type(value) == int or type(value) == float:
                sql += f" AND {key} = {value}"
            else :
                sql += f" AND {key} = '{value}'"
    
    dbConnecter.execute(sql,data)                      
    result = dbConnecter.fetchall() 

    print(sql)
    
    return result
