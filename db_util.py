# coding=utf-8

from config import REDIS_URL, MYSQL_PARAMS

import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_redis_conn():
    # get redis connection.
    redis_host = REDIS_URL.split(':')[1][2:]
    redis_port = REDIS_URL.split(':')[2][:-2]
    redis_conn = redis.Redis(host=redis_host, port=redis_port)
    return redis_conn

def _get_db_url(name):
    return 'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8mb4' % (
        name['user'], name['password'],
        name['host'], name['port'],
        name['db_name']
    )

def get_db_session():
    # connect to mysql.
    db_url = _get_db_url(MYSQL_PARAMS)
    Session = sessionmaker(bind=create_engine(db_url, pool_recycle=3600), autocommit=False)
    session = Session()
    return session

