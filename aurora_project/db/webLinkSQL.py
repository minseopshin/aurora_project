from db import database

dbConnecter = database.dbConnecter

# 조회
def getWebLinkList (data): 
    sql = "SELECT * FROM webLink wl inner join webLinkShare wls on wl.webLinkNo = wls.webLinkNo WHERE 1 = 1 AND wls.read_YN = 1 AND wl.delete_YN = 0"

    if data is not None:
        for key, value in data.items(): 
            if key == "shareUserNo":
                sql += f" AND wls.{key} = {value}"
            elif key == "search" :
                sql += f" AND wl.name like '%{value}%' "
            elif key == "userNo":
                sql += f" AND wl.userNo = {value} "
            else :
                sql += f" AND wl.{key} = '{value}'"

    dbConnecter.execute(sql)                      
    result = dbConnecter.fetchall() 
    print(sql)
    
    return result

# 생성
def createWebLink (data): 

    sql1 = "INSERT INTO webLink (userNo,created_by,name,url,category) VALUES (%s,%s,%s,%s,%s)"
    data1 = (data["userNo"], data["created_by"],data["name"], data["url"], data["category"])

    dbConnecter.execute(sql1, data1)                      
    
    sql2 = "INSERT INTO webLinkShare (webLinkNo,shareUserNo,read_YN,update_YN) VALUES (%s,%s,%s,%s)"
    data2 = (dbConnecter.lastrowid, data["userNo"],1,1)
    
    dbConnecter.execute(sql2, data2)                      
    result = database.mydb.commit()

    print(sql)
    
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

    print(sql)
    
    return result

def getWebLinkShareUserList (data): 
    sql = """
    select 
	    user.userNo ,
	    user.userId ,
	    (select webLinkShare.read_YN  from webLinkShare Where 1=1 and shareUserNo = user.userNo and webLinkShare.webLinkNo = %s) as read_YN,
	    (select webLinkShare.update_YN  from webLinkShare Where 1=1 and shareUserNo = user.userNo and webLinkShare.webLinkNo = %s) as update_YN
    from
	    user
    where
        1 = 1
    """

    if data is not None:
        for key, value in data.items(): 
            if key == "search" :
                sql += f" AND userId like '%{value}%' "

    data = (data["webLinkNo"], data["webLinkNo"])
    dbConnecter.execute(sql,data)                      
    result = dbConnecter.fetchall() 

    print(sql)
    
    return result

def getWebLinkShareList (data):
    sql = """
    select
        *
    from
        webLinkShare
    WHERE
        1 = 1
        AND webLinkNo = %s
        AND shareUserNo = %s
    """

    data = (data["webLinkNo"], data["userNo"])
    dbConnecter.execute(sql,data)                      
    result = dbConnecter.fetchall() 

    print(sql)

    return result



def createWebLinkShare (data): 
    sql = "INSERT INTO webLinkShare (webLinkNo,shareUserNo,read_YN,update_YN) VALUES (%s,%s,%s,%s)"
    dataSet = (data["webLinkNo"], data["userNo"],)

    
    if data["permissionType"] == "update" :
        if data["isChecked"] :
            dataSet += (1,1,)
    elif data["permissionType"] == "read" :
        if data["isChecked"] :
            dataSet += (1,0,)
    
    dbConnecter.execute(sql, dataSet)
    result = database.mydb.commit()

    print(sql)

    return result


def updateWebLinkShare (data, sqlResult): 
    sql = "UPDATE webLinkShare SET "

    if data["permissionType"] == "read":
        if data["isChecked"] :
            sql += f"read_YN = 1"
        elif not data["isChecked"] :
            sql += f"read_YN = 0"
    else :
        if data["isChecked"] :
            sql += f"update_YN = 1"
        elif not data["isChecked"] :
            sql += f"update_YN = 0"


    sql += f" WHERE shareNo = {sqlResult[0]['shareNo']}"

    dbConnecter.execute(sql)                      
    result = database.mydb.commit()

    print(sql)
    
    return result