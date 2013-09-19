import logging
import os

import webapp2
from app.domain.constants import CONSTANTS
import bootstrap

from routes import ROUTES

config = {
    'webapp2_static.static_file_path': './static',
    'globals': {
        'uri_for' : webapp2.uri_for
    },
}
web_app = webapp2.WSGIApplication(routes=ROUTES, config=config, debug=True)

def main():
    if not os.path.exists(CONSTANTS.DB_NAME):
        bootstrap.bootstrap()

    from paste import httpserver
    logging.basicConfig(level=logging.INFO)
    logging.info("Event manager started")
    httpserver.serve(web_app, host='127.0.0.1', port='8080')
    logging.info("Event manager terminated")

if __name__ == '__main__':
    main()