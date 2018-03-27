import MySQLdb
import hashlib
import time
from datetime import datetime
import datetime as dt

def login(username,password):
    mydb = MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='Project')
    m = hashlib.sha256()
    m.update(password.encode('utf-8'))
    hashpassword = m.hexdigest()
    sql = "SELECT * from `user` where username = %s and password = %s"
    data = [username,hashpassword]
    cursor = mydb.cursor()
    cursor.execute(sql,data)
    results = cursor.fetchall()
    row = cursor.rowcount
    if row < 1:
        return "UPworng"
    elif row > 1:
        return "error"
    else:
        return results


def register(username,password,email,tel):
    mydb = MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='Project')
    m = hashlib.sha256()
    m.update(password.encode('utf-8'))
    hashpassword = m.hexdigest()

    sql = "SELECT * from `user` where username = %s"
    data = [username]
    cursor = mydb.cursor()
    cursor.execute(sql,data)
    results = cursor.fetchall()
    row = cursor.rowcount
    if row >= 1:
        return "username used"
    sql = 'INSERT INTO `user`(`username`, `password`, `tel`, `email`) VALUES (%s,%s,%s,%s)'
    data = [username,hashpassword,email,tel]
    cursor = mydb.cursor()
    cursor.execute(sql,data)
    mydb.commit()
    cursor.close()
    return "done"

def adfav(username,status,stock):
    mydb = MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='Project')
    sql = "SELECT * from `trade` where symbol = %s"
    data = [stock]
    cursor = mydb.cursor()
    cursor.execute(sql,data)
    results = cursor.fetchall()
    row = cursor.rowcount
    if row < 1:
        return "No stock"
    if status == 1:#add
        sql = "SELECT * from `favorite` where stock = %s and username = %s"
        data = [stock,username]
        cursor = mydb.cursor()
        cursor.execute(sql,data)
        results = cursor.fetchall()
        row = cursor.rowcount
        if row >= 1:
            return "already add"
        
        sql = 'INSERT INTO `favorite`(`username`, `stock`) VALUES (%s,%s)'
        data = [username,stock]
        cursor = mydb.cursor()
        cursor.execute(sql,data)
        mydb.commit()
        cursor.close()
        return "add done"
    elif status == 0:#del
        sql = "SELECT * from `favorite` where stock = %s and username = %s"
        data = [stock,username]
        cursor = mydb.cursor()
        cursor.execute(sql,data)
        results = cursor.fetchall()
        row = cursor.rowcount
        if row < 1:
            return "Deleted"
        sql = 'DELETE FROM `favorite` WHERE stock = %s and username = %s'
        data = [stock,username]
        cursor = mydb.cursor()
        cursor.execute(sql,data)
        mydb.commit()
        cursor.close()
        return "del done"
    else:
        return "error"

def showfav(username):
    mydb = MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='Project')
    sql = "SELECT * from `favorite` where  username = %s"
    data = [username]
    cursor = mydb.cursor()
    cursor.execute(sql,data)
    results = cursor.fetchall()
    row = cursor.rowcount
    if row < 1:
        return "No stock"
    return results

def infostock(stock,date):
    date = datetime.strptime(date, '%Y-%m-%d').date()
    mydb = MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='Project')
    sql = "SELECT * from `trade` where  symbol = %s and date = %s"
    for x in range(0,6):
        data = [stock,str(date)]
        cursor = mydb.cursor()
        cursor.execute(sql,data)
        results = cursor.fetchall()
        row = cursor.rowcount
        if row >= 1:
            return results
        date -= dt.timedelta(days=1)
    return "stock close"