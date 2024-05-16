import pymysql
import pymysql.cursors

_db = pymysql.connect(
        host='KHSeo.mysql.pythonanywhere-services.com',
        port=3306,
        user='KHSeo',
        password='tjrbgjs13^',
        db='KHSeo$ubion'
        )

cursor = _db.cursor(pymysql.cursors.DictCursor)

create_user = """
        CREATE TABLE IF NOT EXISTS `user` (
        id VARCHAR(32) PRIMARY KEY,
        password VARCHAR(64) NOT NULL,
        name VARCHAR(32) NOT NULL
        )
    """

# Execute the SQL query
cursor.execute(create_user)
# Commit the transaction
_db.commit()
# Close the connection
_db.close()

# Confirmation
print('Table created successfully.')
