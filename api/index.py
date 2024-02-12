from http.server import BaseHTTPRequestHandler
import json
import socketserver
from http import HTTPStatus
from urllib.parse import parse_qs
import cgi

 
class handler(BaseHTTPRequestHandler):

	def do_GET(self):

		# respond with a simple html page with a form that posts a file to the same url
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
        self.wfile.write(open('index.html', 'r').read())
		return
	
	# receive a IFC file in a post request and return a json with the IFC file name
	def do_POST(self):

		# parse as multipart/form-data
		form = cgi.FieldStorage(
			fp=self.rfile,
			headers=self.headers,
			environ={'REQUEST_METHOD':'POST',
					'CONTENT_TYPE':self.headers['Content-Type'],
					})
		
		# check if the file is in the form
		if "file" not in form:
			self.send_response(400)
			self.send_header('Content-type','application/json')
			self.end_headers()
			self.wfile.write(json.dumps({"message": "No file found"}).encode('utf-8'))
			return
		
		# get the file from the form
		fileitem = form["file"]
		
		# check if the file is in the form
		if fileitem.filename == '':
			self.send_response(400)
			self.send_header('Content-type','application/json')
			self.end_headers()
			self.wfile.write(json.dumps({"message": "No file found"}).encode('utf-8'))
			return
		
		# read the file
		post_data = fileitem.file.read()

		# write the content to a file
		filename = "ifc_file.ifc"
		with open(filename, "wb") as f:
			f.write(post_data)
		
		my_list = process_file(filename)

		# respond with json {"message": "Hello World!"}
		self.send_response(200)
		self.send_header('Content-type','application/json')
		self.end_headers()

		# json.stringify({"my_list": my_list})
		self.wfile.write(json.dumps({"my_list": my_list}).encode('utf-8'))

		return


import ifcopenshell
import ifcopenshell.util.element

def process_file(filename):
	#model = ifcopenshell.open('./Wellness_center_Sama.ifc')
	model = ifcopenshell.open(filename)
	#print(model.schema)
	"""
	walls = model.by_type('IfcWall')
	print(len(walls))

	for wall in walls:
		# Walls are typically located on a storey, equipment might be located in spaces, etc
		container = ifcopenshell.util.element.get_container(wall)
		# The wall is located on Level 01
		print(f"The wall is located on {container.Name}")
	"""

	my_list = []
	for storey in model.by_type("IfcBuildingStorey"):
			elements = ifcopenshell.util.element.get_decomposition(storey)
			print(f"There are {len(elements)} located on storey {storey.Name}, they are:")
			for element in elements:
					#print(element.Name)
					my_list.append(element.Name)
	
	return my_list



if __name__ == '__main__':
	with socketserver.TCPServer(("", 8080), handler) as httpd:
		print("serving at port", 8080)
		httpd.serve_forever()
		
	# start the server
	# from http.server import HTTPServer
	# server = HTTPServer(('', 8080), handler)
	# server.serve_forever()
