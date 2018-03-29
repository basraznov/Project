from flask import request
from flask import Flask,session,redirect,Response
import os
import web as wb
import random
import json

app = Flask(__name__)

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        if "username" in request.form and "password" in request.form:
            username =  request.form["username"]
            password =  request.form["password"]
            data = wb.login(username=username,password=password)
            if data == 'UPworng':
                m = '{"status":"Username or password Wrong"}'
            elif data == 'error':
                m = '{"status":"Something error"}'
            else:
                session["user"] = data[0][0]
                session["key"] = random.randint(0,10)
                m = '{"status":"done"}'
        else:
            m = '{"status":"error"}'
    else:
        m = '{"status":"NotPost"}'

    res = Response(response=m,
                status=200,
                mimetype='application/json')
    return res

@app.route("/index")
def index():
    if 'user' in session:
        return session["user"]+'<br><br><form class="form-inline my-2 my-lg-0" action="/logout" method="get"> <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Logout</button> </form>'
    else:
        return '<form action="/login" method="post">  <input type="text" placeholder="Enter Username" name="username" required>     <input type="password" placeholder="Enter Password" name="password" required>   <button type="submit">Login</button></form>'

@app.route("/logout")
def logout():
    session.clear()
    if 'user' in session:
        return "session still exist: "+session["user"]
    else:
        return "session was clear"

@app.route("/register",methods=["POST"])
def register():
    if request.method == "POST":
        if "username" in request.form and "password" in request.form and "tel" in request.form and "email" in request.form:
            username = request.form["username"]
            password = request.form["password"]
            email = request.form["email"]
            tel = str(request.form["tel"])
            insert = wb.register(username = username, password = password,email = email,tel=tel)
            if insert == 'done':
                m = '{"status":"done"}'
            if insert == 'username used':
                m = '{"status":"username is used"}'
        else:
            m = '{"status":"Error"}'
    else:
        m = '{"status":"NotPost"}'
    
    res = Response(response=m,
                    status=200,
                    mimetype='application/json')
    return res


@app.route("/adfav",methods=["POST"])
def adfav():
    if request.method == "POST": 
        if 'user' in session and "stock" in request.form and "status" in request.form and session["user"] != None:
            stock = request.form["stock"]
            status = int(request.form["status"])
            user = session["user"]
            k = wb.adfav(username=user,status=status,stock=stock)
            if k == "No stock":
                m = '{"status":"No Stock"}'
            elif k == "already add":
                m = '{"status":"You have this stock"}'+session["user"]
            elif k == "add done":
                m = '{"status":"Done"}'
            elif k == "Deleted":
                m = '{"status":"You don\'t have this stock in list"}'
            elif k == "del done":
                m = '{"status":"Done"}'
            else:
                m = '{"status":"Error"}'
        else:
            m = '{"status":"Require login or wrong parameter"}'
    else:
        m = '{"status":"NotPost"}'
    res = Response(response=m,
                    status=200,
                    mimetype='application/json')
    return res

@app.route("/showfav",methods=["GET"])
def showfav():
    if request.method == "GET":
        user = session["user"]
        k = wb.showfav(username=user)
        if k == "No stock":
            m = '{"status":"No stock in list"}'
        else:
            m = '{"stock":['
            for x in k:
                m += '"'+x[1]+'"'
                if x != k[-1]:
                    m += ','
                else:
                    m += ']}'
    else:
        m = '{"status":"NotGet"}'
    res = Response(response=m,
                    status=200,
                    mimetype='application/json')
    return res

@app.route("/infostock",methods=['POST'])
def infostock():
    if request.method == "POST":
        if 'user' in session and 'stock' in request.form and 'date' in request.form:
            stock = request.form["stock"]
            date = request.form["date"]
            k = wb.infostock(stock,date)
            if k == "stock close":
                m = '{"status":"stock is not upto date or has been code"}'
            m = '{"LastUpDate":"'+str(k[0][0])+'","open":"'+str(k[0][2])+'","high":"'+str(k[0][3])+'","low":"'+str(k[0][4])+'","last":"'+str(k[0][5])+'"}'
        else:
            m = '{"status":"Require login or wrong parameter"}'
    else:
        m = '{"status":"NotPost"}'
    res = Response(response=m,
                    status=200,
                    mimetype='application/json')
    return res

if __name__ == '__main__':
    app.secret_key = "askljir8(#&&-3'(3asdfa;sjkkl"
    app.config.update(
        SESSION_REFRESH_EACH_REQUEST = False
    )
    app.run(host="0.0.0.0", port=8000)





