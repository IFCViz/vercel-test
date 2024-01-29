from http.server import BaseHTTPRequestHandler
 
class handler(BaseHTTPRequestHandler):

	def do_GET(self):

		# respond with json {"message": "Hello World!"}
		self.send_response(200)
		self.send_header('Content-type','application/json')
		self.end_headers()
		self.wfile.write('{"message": "Hello Anders!"}'.encode('utf-8'))

		"""
		self.send_response(200)
		self.send_header('Content-type','text/plain')
		self.end_headers()
		self.wfile.write('Hello, world!'.encode('utf-8'))
		"""
		return
