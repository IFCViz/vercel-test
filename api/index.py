from http.server import BaseHTTPRequestHandler
import json
 
class handler(BaseHTTPRequestHandler):

	def do_GET(self):

		# respond with a simple html page with a form that posts a file to the same url
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write('<html><body><form action="/" method="post" enctype="multipart/form-data"><input type="file" name="file"><input type="submit"></form></body></html>'.encode('utf-8'))

		return
	
	# receive a IFC file in a post request and return a json with the IFC file name
	def do_POST(self):

		# get the content length of the request
		content_length = int(self.headers['Content-Length'])

		# read the content of the request
		post_data = self.rfile.read(content_length)

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
	walls = model.by_type('IfcWall')
	print(len(walls))

	for wall in walls:
		# Walls are typically located on a storey, equipment might be located in spaces, etc
		container = ifcopenshell.util.element.get_container(wall)
		# The wall is located on Level 01
		print(f"The wall is located on {container.Name}")

	my_list = []
	for storey in model.by_type("IfcBuildingStorey"):
			elements = ifcopenshell.util.element.get_decomposition(storey)
			print(f"There are {len(elements)} located on storey {storey.Name}, they are:")
			for element in elements:
					#print(element.Name)
					my_list.append(element.Name)
	
	return my_list
