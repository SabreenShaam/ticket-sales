DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'ticketing_db'
DB_HOST = 'localhost'
# DB_HOST = 'mysql'
DB_PORT = '3306'

JWT_SECRET_KEY = '1q2w3e4r5t6y7u8i9o'

DB_ENGINE = 'mysql+pymysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + ':' + DB_PORT + '/' + DB_NAME
