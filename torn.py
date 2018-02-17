import sys
import os
from tornado.options import options, define, parse_command_line
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
from tornado import websocket
from django.core.wsgi import get_wsgi_application
from tornado.httpclient import AsyncHTTPClient

define('port', type=int, default=8888)

class MainHandler(tornado.web.RequestHandler):

	def handle_response(self, response):
		if response.error:
			print("Error: %s" % response.error)
		else:
			print(response.body)

	@tornado.web.asynchronous
	def get(self):
		http_client = AsyncHTTPClient()
		post_data = { 'username': 'ivanmarkov1997', 'password': 'i4611366968'} #A dictionary of your post data
		body = tornado.escape.json_encode(post_data)
		headers = {}
		headers['Content-Type'] = 'application/json'
		http_client.fetch("http://127.0.0.1:8080/auth/token", self.handle_response, method='POST', headers=headers, body=body)

class WSHandler(websocket.WebSocketHandler):

	clients = []

	#prevent from Http-403 Forbidden
	def check_origin(self, origin):
		return True

	def open(self):
		print("WS opened")
		self.clients.append(self)

	def on_message(self, message):
		print(message)
		for client in self.clients:
			client.write_message(message)

	def on_close(self):
		print("WS closed")
		self.clients.remove(self)

def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'joyle.settings' # TODO: edit this
    sys.path.append('./joyle') # path to your project if needed

    parse_command_line()

    wsgi_app = get_wsgi_application()
    container = tornado.wsgi.WSGIContainer(wsgi_app)

    tornado_app = tornado.web.Application(
        [
            ('/tornado', MainHandler),
            ('/websocket', WSHandler),
            ('.*', tornado.web.FallbackHandler, dict(fallback=container)),
        ])

    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()