import MySQLdb
import hashlib

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
    pass
    sql = 'INSERT INTO `user`(`username`, `password`, `tel`, `email`) VALUES (%s,%s,%s,%s)'
    data = [username,hashpassword,email,tel]
    cursor = mydb.cursor()
    cursor.execute(sql,data)
    mydb.commit()
    cursor.close()
    return "done"