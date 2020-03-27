class AppConfig():
    DEBUG = True
    SECRET_KEY = b">\x81'\xd1\x10-\x95\xb6\x12Nh?8\xc7\xf9\xe1"
    HTTP_PORT = 8080

MYSQL_PARAMS = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'test',
    'password': 'test_passwd',
    'db_name': 'gh',
    'charset': 'utf8mb4'
}

REDIS_URL = 'redis://127.0.0.1:6379/0'