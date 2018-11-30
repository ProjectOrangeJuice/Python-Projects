import socket, ssl, time,sys


import sqlite3 as lite



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def deal(c):
	print "on deal"
	c.send("APP! 8613498915822164439764937756304892199891906460908222656354978180857455234237452 \n")
	c.send("AUTH JUGN-INFO_pass\n")
	
	for line in readlines(c):
		print "line is: ",line
		code = line[:4].upper()
		print "stage one code: ",code
		if(code != "MSGS"):
			print "not a message"
			continue
		line = line[5:len(line)].split("_",2) 
		name = line[0]
		code = line[1][:4]
		line = line[1][5:len(line[1])]
		
		
		
		print "code %s  \n name %s line %s" %(code,name,line)
		if(code=="ADDS"):
			print "adds"
			try:
				values = line.split(":")
				print values[1]
			except:
				print str(sys.exc_info())
				continue
			addToDatabase(name,values[0].upper(),values[1])
			
		if(code=="DELT"):
			delFromDatabase(name,line.upper())
		if(code=="LIST"):
			
			displayContacts(name)
		if(code=="DALL"):
			DALL(name)
			
			
			
			


def addToDatabase(account,contact,name):
	
	print "account: ",account
	account = account[:4]
	con = lite.connect('system.db')
	with con:    
		cur = con.cursor()    
		cur.execute("INSERT INTO contacts(account,contact,name) VALUES(?,?,?)",(account,contact,name))
		print "added "
		

def delFromDatabase(account,contact):
	print "account: ",account
	account = account[:4]
	con = lite.connect('system.db')
	with con:    
		cur = con.cursor()    
		cur.execute("DELETE FROM contacts WHERE account=? and contact=?",(account,contact))
		print "deleted "
		
		

def displayContacts(account):
	print "account: ",account
	account2 = account[:4]
	print "account2: ",account2
	con = lite.connect('system.db')
	with con:    
		cur = con.cursor()    

		cur.execute("SELECT * FROM contacts WHERE account=? ",(account2,))
		rows = cur.fetchall()
		values = ""
		run = False
		for row in rows:
			run = True
			if(values == ""):
				values = row[1]+":"+row[2]
			else:
				values = values+"~"+row[1]+":"+row[2]
		if(run):
			s.send("SEND "+account+"_0_LIST_"+values+"\n")


def DALL(username):
	print "Delete all for: ",username[:4]
	u = username[:4]
	con = lite.connect('system.db')
	with con:    
		cur = con.cursor()    
		cur.execute("DELETE FROM contacts WHERE account=? ",(u,))
		print "deleted all!"
		s.send("SEND "+username+"_000_DALL finished\n")
		






def readlines(sock, recv_buffer=1024, delim='\n'):
	buffer = ''
	data = True
	while data:
		try:
			data = sock.recv(recv_buffer)
			
			buffer += data
	
			while buffer.find(delim) != -1:
				line, buffer = buffer.split('\n', 1)
				yield line
		except:
			
			return 

	return









########################################################################




while(True):
		#try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s = ssl.wrap_socket(s,
                           ca_certs="server.crt",
                           cert_reqs=ssl.CERT_REQUIRED)
		s.connect(('192.168.1.19', 2030))
		deal(s)
		#except:
		#	print "Can't connect: "+str(sys.exc_info())
		#	time.sleep(5)
		






