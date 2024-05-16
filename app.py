from flask import Flask, request, render_template, redirect, url_for, session
import pymysql
import pymysql.cursors
from datetime import timedelta
from static.python import querys
# 환경 변수 dotoenv 로드
from dotenv import load_dotenv
import os
# database.py 안에 있는 MYDB class load
from static.python.database import MYDB

# .env파일 로드
load_dotenv()




app = Flask(__name__)

app.secret_key = load_dotenv('secret_key')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=10)


# MYDB class 생성
mydb = MYDB(
    os.getenv('host'),
    int(os.getenv('port')),
    os.getenv('user'),
    os.getenv('password'),
    os.getenv('db_name')
)



@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/index')
    else:
        try:
            _state = request.args['state']
        except:
            _state = 1
        return render_template('login.html', state = _state)
    


@app.route('/main', methods = ['post'])
def main():
    _id = request.form['input_id']
    _pass = request.form['input_pass']
    print(f'유저 id : {_id}  password : {_pass}')
    db_result = mydb.db_execute(querys.login_query, _id, _pass)

    if db_result:
        session['user_id'] = _id
        session['user_pass'] = _pass
        return redirect('/index')
    else:
        return redirect('/?state=2')
    
@app.route('/index')
def index2():
    # 세션에 데이터가 존재한다면 return main.html
    if 'user_id' in session:
        return render_template('main.html')
    # 세션에 데이터가 없다면 return login page
    else:
        return redirect('/') 

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/check_id', methods = ['post'])
def check_id():
    _id = request.form['input_id']
    print(f"/check_id[post] ->유저 id : {_id}")
    db_result = mydb.db_execute(querys.check_id_query, _id)
    if db_result:
        result = "0"
    else:
        result = "1"
    return result

@app.route('/signup2', methods = ['post'])
def signup2():
    _id = request.form['input_id']
    _pass = request.form['input_pass']
    _name = request.form['input_name']
    print(f"/signup2[post] -> 유저 ID : {_id}  password : {_pass}")
    try:
        db_result = mydb.db_execute(querys.signup_query, _id, _pass, _name)
        print(db_result)
    except:
        db_result = 3
    if db_result == 3:
        return redirect(f'/?state={db_result}')
    else:
        return redirect('/')
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

app.run(debug=True)