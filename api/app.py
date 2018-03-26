from flask import request
from flask import Flask,session,redirect
import os
import web as wb

app = Flask(__name__)

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username =  request.form['username']
            password =  request.form['password']
            data = wb.login(username=username,password=password)
            if data == "UPworng":
                return "{'status':'Username or password Wrong'}"
            elif data == "error":
                return "{'status':'Something error'}"
            else:
                session['user'] = data[0][0]
            return "{'status':'done'}"
        else:
            return "{'status':'error'}"
    else:
        return "{'status':'NotPost'}"

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@app.route('/register',methods=['POST'])
def register():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form and 'tel' in request.form and 'email' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            tel = str(request.form['tel'])
            insert = wb.register(username = username, password = password,email = email,tel=tel)
            if insert == "done":
                return "{'status':'done'}"
            if insert == "username used":
                return "{'status':'username is used'}"
        else:
            return "{'status':'error'}"
    else:
        return "{'status':'NotPost'}"

if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(host='0.0.0.0', port=8000)