import logging

import webapp2

from routes import ROUTES

config = {'webapp2_static.static_file_path': './static'}
web_app = webapp2.WSGIApplication(routes=ROUTES, config=config, debug=True)

def main():
    from paste import httpserver
    logging.basicConfig(level=logging.INFO)
    logging.info("Event manager started")
    httpserver.serve(web_app, host='127.0.0.1', port='8080')
    logging.info("Event manager terminated")

if __name__ == '__main__':
    main()