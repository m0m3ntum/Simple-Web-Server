import sys,socket,os,threading
from threading import Thread


host = socket.gethostname()
port = 8080
BUFFERSIZE = 65536

#------------------ TRYING TO CREATE THE CLIENT SOCKET ------------------#
try: #here we try to connect to the server. if not we get an exception
	s = socket.socket() #creating socket
	s.connect((host,port))
except socket.error, (message):#Here we get the exception, if any

	if s:
		s.close()
	print "The socket could not be opened!!! Reason: " , message
	sys.exit(1) #exit of the program
print 'Connection established! You may send messages!\n'
#------------ AFTER HERE THE CLIENT SOCKET IS READY ------------#



isForked = False #init that we did not fork for now
menu = "1-> Get an HTML file\n2-> Get an HTML file using CGI(with GET)\n3-> Get an HTML file using CGI(with POST)\n"
menu += "4-> Get the list of files that htmlfolder contains\n5-> Send false folder (GET 404 Error)\n"
menu += "0-> exit\n\n"


while s:
	
	if (isForked == False):
		pid = os.fork()#Create an new instance of this
		isForked = True 
	if (pid == 0): #if father		
		choice = raw_input(menu)
		packet=""
		if (choice ==str(1)):
			packet =  """GET ./htmlfolder/test.html HTTP/1.0'
				  'Date : Sun, 17 Jan 2016 10:00:00 GMT+2'
				  'User-Agent: Mozilla 34'
				  '',
				  'EOF' """
		elif(choice==str(2)):
			packet = """GET ./cgi-bin/my_command.py?name=toto&val=10 HTTP/1.0'
				  'Date : Sun, 17 Jan 2016 10:00:00 GMT+2'
				  'User-Agent: Mozilla 34'
				  '',
				  'EOF' """
		elif(choice==str(3)):
			packet = """POST ./cgi-bin/my_command.py?name=toto&val=10 HTTP/1.0'
				  'Date : Sun, 17 Jan 2016 10:00:00 GMT+2'
				  'User-Agent: Mozilla 34'
				  '',
				  'EOF' """
		elif(choice==str(4)):
			packet = """GET ./htmlfolder/ HTTP/1.0'
				  'Date : Sun, 17 Jan 2016 10:00:00 GMT+2'
				  'User-Agent: Mozilla 34'
				  '',
				  'EOF' """
		elif(choice==str(5)):
			packet = """GET ./htmlfol/ HTTP/1.0'
				  'Date : Sun, 17 Jan 2016 10:00:00 GMT+2'
				  'User-Agent: Mozilla 34'
				  '',
				  'EOF' """

		elif(choice==str(0)):
			packet = "exit"
			
		s.send(packet)
		if (packet == "exit"): #Closing Father
			print "The connection Terminated! The program will close!\n"
			s.close()
			sys.exit(0)
		print "Packet Sent!"
	else:	#if child
		reply = s.recv(BUFFERSIZE)
		if (reply == "exit"): #Closing Child
			s.close()
			sys.exit(0)
		print "\n\n--------------------------------------------"
		print 'Reply from Server-->\n',repr(reply)
		print "--------------------------------------------"
		print "\n\n",menu
