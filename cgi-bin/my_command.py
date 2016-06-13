#!/usr/bin/python

import cgi, sys, os
import cgitb; 

cgitb.enable()


fo = open("temp.html", "wb")#create a temp html file that is holding the data to send to the client
fo.write("""
<!DOCTYPE html>\n
<html>

<head><meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>
<title>CGI Document</title></head>

<body>

<h1> Example </h1>
   """)




if os.getenv("REQUEST_METHOD") == 'GET':
    	form = cgi.FieldStorage()
	if "name" not in form or "val" not in form:
		fo.write("<h2> THERE WERE NOT ATTRIBUTES!!! </h2>\n")
	else:	
		name = form.getvalue('name')
		fo.write("<h2> The name of the student is "+name+" </h2>\n")
    		age = form.getvalue('val')
		fo.write("<h2> The age of the student is "+age+" </h2>")
else:	
	fo.write("<h2> THERE WERE NOT ATTRIBUTES!!! </h2>\n")
		

fo.write("""
</body>
</html>
   """)

fo.close()# closing the file
