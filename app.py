# encoding=utf-8
import logging
import time

import traceback
from datetime import timedelta
from flask import Flask, jsonify
from flask import g, request

from config import AppConfig
from db_util import get_db_session

from flask import current_app

def create_app():
    app = Flask(__name__)
    config = AppConfig()
    app.config.from_object(config)
    app.logger.setLevel(logging.INFO)
    app.app_context().push()
    

    @app.errorhandler(Exception)
    def exception_handler(e):
        traceback.print_exc()
        current_app.logger.error(str(e))
        # error_code.
        g.code = 1003
        http_code = 500
        error_resp = {'error_code': g.code, 'msg': str(e)}
        return jsonify(error_resp), http_code 

    @app.before_request
    def before_request():
        # init db session.
        g.db = get_db_session()
        g.code = 0

    @app.after_request
    def after_request(response):
        code = response.status_code
        if hasattr(g, 'code'):
            code = g.code

        # close db session.
        if g.db is not None:
            if code != 0 and code != 200:
                # rollback if failed.
                g.db.rollback()
            else:
                g.db.commit()
            g.db.close()
        
        current_app.logger.info("[Request Log]" + request.path + ' [data] ' + str(request.data))
        
        return response
    return app


app = create_app()


from feeds_route import *

if __name__ == '__main__':
    config = AppConfig()
    app.run(host='0.0.0.0', port=config.HTTP_PORT)
