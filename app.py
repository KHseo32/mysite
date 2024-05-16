from flask import Flask, request, render_template, redirect, url_for, session
import pymysql
import pymysql.cursors
from datetime import timedelta
app = Flask(__name__)

app.secret_key = 'ABC'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=10)

def db_execute(query, *data):
    # 데이터베이스와 연결
    _db = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='1234',
        database='ubion'
    )
    # Cursor 생성
    cursor = _db.cursor(pymysql.cursors.DictCursor)
    # 매개변수 query, data를 이용하여 질의
    cursor.execute(query, data)
    # query가 select라면 결과값을 변수(result)에 저장
    if query.strip().lower().startswith('select'):
        result = cursor.fetchall()
    # query가 select가 아니라면 DB server와 동기화하고 변수(result)는 Query OK 문자를 대입
    else:
        _db.commit()
        result = "Query OK"
    # 데이터비에서 서버와의 연결 종료
    _db.close()
    # 결과(result)를 되돌려준다.
    return result




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

    login_query = """
        select
        *
        from
        user
        where
        id = %s
        and
        password = %s
    """

    db_result = db_execute(login_query, _id, _pass)

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
    check_id_query = """
        select * from user
        where id = %s
    """
    db_result = db_execute(check_id_query, _id)
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
    insert_user_query = """
     insert into `user`
     values (%s, %s, %s)
    """
    try:
        db_result = db_execute(insert_user_query, _id, _pass, _name)
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