
import socket, sys, os,  commands, threading
from threading import Thread

import requests
import subprocess

#define host ip & port
port = 8080    #the port that the server is listening     
BUFFERSIZE = 65536  #64 Mb buffer
cmd = ""
host = socket.gethostname()


#------------------ TRYING TO CREATE THE SERVER SOCKET ------------------#
try: 
	s = socket.socket()
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host,port))
except socket.error, (message):#Here we get the exception, if any

	if s:
		s.close()
	print "The socket could not be opened!!! Reason: " , message
	sys.exit(1) #exit of the program
print 'Server is ready!\n'	
#------------ AFTER HERE THE SERVER SOCKET IS READY ------------#



#------------------- FUNCTION THAT SEPERATES A PACKET -------------------#
def packet_splitter(packet):	#Function where a packet is divided in several parts
				#example # GET /my_command.cgi?name=toto&val=10 HTTP/1.0
	s = packet.split(" ")
	path = s[1] #GET THE PART WITH URL THAT HAVE THE ATTRIBUTES

	if(path.split("?")):
		p = path.split("?")
		path = p[0] #GET THE PATH OF THE FILE

	return  path #RETURN THE PATH OF THE FILE
#----------------- END FUNCTION THAT SEPERATES A PACKET -----------------#




#------------------- FUNCTION THAT SEPERATES A PACKET -------------------#
def url_splitter(packet):	#Function where a packet is divided in several parts
			#example # GET /my_command.cgi?name=toto&val=10 HTTP/1.0								

	s = packet.split(" ")
	method = s[0] #GET THE PART METHOD (POST/GET)
	path = s[1] #GET THE PART OF FILE AND ATTRIBUTES

	p = path.split("?") #SPLITS PATH
	print "path is" + str(p)
	print method
	path = p[0] #GET PATH
	args = p[1] #GET ATTRIBUTES
	return (method,path,args) #RETURN ALL
#------------------- FUNCTION THAT SEPERATES A PACKET -------------------#




#---------------------- FUNCTION CREATE RAPPELS ----------------------#
def create_rappel(catalog,files):
	rappel = """<HTML>
			<HEAD>
				<TITLE>DIRECTORY CONTENT</TITLE>
			</HEAD>
			<BODY>
				<UL>
"""
	for f in files:
		if f.endswith(".html"): #if the file is html
			rappel += "<LI>"
			rappel += "<A HREF=\""
			rappel += catalog	
			rappel += f
			rappel += "\">"	
			rappel += f
			rappel += "</A></LI>"			
	
	rappel += """		</UL> 
			</BODY>
		</HTML>
			
"""	
	return rappel

#---------------------- END FUNCTION CREATE RAPPELS ----------------------#





#---------------------- FUNCTION OF SERVER ----------------------#
def server(client, address): #Define functions that get the messages and send them to all
	print "Accepted connection from: ", address #Shows who is connected

	while client:
		packet = client.recv(BUFFERSIZE) #receiving the message from the client
		print  packet

		if (packet == "exit"):#IF the client request to close connection
			print "GET END COMMAND.Terminating Connection..."
			client.send("exit") #reply to the client to exit
			client.close() #kill socket
			break; #END the while loop
		path = packet_splitter(packet)
		if (os.path.exists(path) | os.path.isfile(path) ): #IF path or file exist
			if os.path.isfile(path): # IF path is file
				if path.endswith('.html'): #IF the file is html file
					MIME_TYPE = "Content-Type:text/html" 
					size = os.stat(path) #Get the size of the html file
					cont_length = "Content-Length: " + str(size.st_size)

					with open(path) as fl: #READ THE HTML FILE
					    content = fl.read()

					fl.close
					status = "HTTP 200 OK\n"	
					curdate = "Date : Sun, 17 Jan 2016 10:00:00 GMT+2\n"
					mimeVer = "MIME-Version: 1.0\n"
					header = status+curdate+mimeVer+MIME_TYPE+"\n"+cont_length+"\n\n"		 		
					client.send(header) #send response header
					client.send(content) #send response data
					print "HTML file was sent to: ", address 
					print "\n\n"

				elif path.endswith('.py'): #CGI section
					method,path,args = url_splitter(packet)
					#set environmental values for cgi communication 
					os.environ['QUERY_STRING'] = args 
					os.environ['REQUEST_METHOD'] = method
					output = execfile(path) # execute cgi on server
					print "CGI file run on server!"					
					with open("temp.html") as fl: #READ THE HTML FILE that created from cgi
					    content = fl.read()

					fl.close
					status = "HTTP 200 OK\n"	
					curdate = "Date : Sun, 17 Jan 2016 10:00:00 GMT+2\n"
					mimeVer = "MIME-Version: 1.0\n"
					MIME_TYPE = "Content-Type:text/html"
					size = os.stat(path)
					cont_length = "Content-Length: " + str(size.st_size)
					header = status+curdate+mimeVer+MIME_TYPE+"\n"+cont_length+"\n\n"		 		
					client.send(header) #send response header
					client.send(content) #send response data
					print "HTML file was sent to: ", address 
					print "\n\n"					
					#os.remove("./cgi-bin/temp.html") #removing the temp html file
			else: # if path is just a path
				cmd = 'ls ' + path
				print cmd
				status, output = commands.getstatusoutput(cmd)
				temp =  str(output)			
				files = temp.split("\n")
				rappel = create_rappel(path,files)
				#print rappel
				#build response
				response = "HTTP 200 OK\n" 				
				response += "Date : Sun, 17 Jan 2016 10:00:00 GMT+2"
				response += "MIME-Version: 1.0"
				response += "MIME_TYPE:path"
				response += rappel
					
				client.send(response)
				print "HTML file was sent to: ", address 
		else: # not found as file
			response = "ERROR 404"
			client.send(response) #send response	
#-------------------END FUNCTION OF SERVER -------------------#




#---------------------- MAIN FUNCTION ----------------------#
s.listen(3)
print "Press <Ctrl+c> to exit the program!\n"
while s:
	print "Server is listening for connections..."
	client, address = s.accept()
	serverthread = threading.Thread(target=server, args = (client,address))
	serverthread.start()
#s.close()
#---------------------- MAIN FUNCTION ----------------------#


