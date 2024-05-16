import pymysql
import pymysql.cursors

_db = pymysql.connect(
        host = 'KHSeo.mysql.pythonanywhere-services.com',
        port = 3306,
        user = 'KHSeo',
        password = 'tjrbgjs13^',
        db = 'KHSeo$ubion'
        )

cursor = _db.cursor(pymysql.cursors.DictCursor)

create_user = """
        create table
        if exists
        user(
        id varchar(32) primary key,
        password varchar(64) not null,
        name varchar(32) not null
        )
    """
# sql 쿼리문 실행
cursor.execute(create_user)
# 동기화
_db.commit()
# 서버와의 연결 종료
_db.close()

# 확인
print('table 생성 완료')