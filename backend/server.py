import os
import traceback

import tornado.ioloop
import tornado.web

from ahapiclient import AHClient
from ahapiclient.exceptions import AHBaseException

TOKEN = os.environ.get('TOKEN', 'Your token here')

class BaseHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

class MainHandler(BaseHandler):
    def initialize(self, ah_client):
        self.ah_client = ah_client

    def get(self, profile_id):
        try:
            profile = self.ah_client.get_profile(profile_id)
        except AHBaseException as e:
            traceback.print_exc()

            self.set_status(500)
            self.write('Cannot get profile from AmazingHiring')

        else:
            self.set_status(200)
            self.write(profile)

            ############################
            #                          #
            #   Write your logic here  #
            #                          #
            ############################
        
        finally:
            self.finish()

def make_app():
    ah_client = AHClient(TOKEN)

    return tornado.web.Application([
        (r"/save_profile/(.*)", MainHandler, dict(ah_client=ah_client)),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()