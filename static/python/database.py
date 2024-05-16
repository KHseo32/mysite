# mysql 서버와의 연결부터 query문 질의까지 class 생성

import pymysql

class MYDB:
    def __init__(
            self, _host, _port, _user, _pass, _db
    ):
        self.host = _host
        self.port = _port
        self.user = _user
        self.password = _pass
        self.db = _db
    def db_execute(self, query, *data):
    # 데이터베이스와 연결
        _db = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.db
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