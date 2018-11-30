import socket, ssl, time,sys


import sqlite3 as lite






def deal(c):
	print "on deal"
	c.send("AUTH MONI-INFO_PASS\n")
	
	for line in readlines(c):
		print "line is: ",line
		code = line[:4]
		line = line[5:len(line)]
		
		
		if(code=="LIST"):
			makeTheList(line)
		
		elif(code=="NEW!"):
			data = line.split("_")
			con = lite.connect('store.db')
			with con:    
				cur = con.cursor()    
				cur.execute("INSERT INTO store(ids,connection,address) VALUES(?,?,?)",(data[0],data[2],data[1]))

		elif(code=="USER"):
			data = line.split("_")
			con = lite.connect('store.db')
			with con:    
				cur = con.cursor()    
				cur.execute("UPDATE store SET username=? WHERE  ids=?",(data[1],data[0]))
		elif(code=="APP!"):
			data = line.split("_")
			con = lite.connect('store.db')
			with con:    
				cur = con.cursor()    
				cur.execute("UPDATE store SET app=? WHERE  ids=?",(data[1],data[0]))

		elif(code=="DEL!"):
			data = line.split("_")
			con = lite.connect('store.db')
			with con:    
				cur = con.cursor()    
				cur.execute("DELETE FROM store WHERE ids=?",(data[0],))


		elif(code=="SECR"):
			print "secure"
			data = line.split("_")
			con = lite.connect('store.db')
			with con:    
				cur = con.cursor()    
				cur.execute("UPDATE store SET secure='yes' WHERE  ids=?",(data[0],))










def makeTheList(line):
	con = lite.connect('store.db')
	with con:    
		cur = con.cursor()    
		cur.execute("DELETE FROM store")
	
	lines = line.split("_")
	print "********************"
	print lines
	print "***************"
	num = dict(item.split("::") for item in lines[0].split(";"))
	userlist = dict(item.split("::") for item in lines[1].split(";"))
	connections = dict(item.split("::") for item in lines[2].split(";"))
	print "connections: ",connections
	print "num: ",num
	print "userlist: ",userlist
	
	with con:    
		cur = con.cursor()    
		names = {}
		for ids,connection in connections.iteritems():
			names[ids] = ""
		
		
		
		for name,connection in userlist.iteritems():
			username = name[:9]
			ids = name[9:len(name)]
			names[ids] = username
			
		
		
		
		
		for ids,username in names.iteritems():
				
			cur.execute("INSERT INTO store(ids,address,app,username) VALUES(?,?,?,?)",(ids,"?","?",username))



def addNewId(address,conn,ids,times):
	con = lite.connect('system.db')
	
	with con:    
		cur = con.cursor()    
		cur.execute("INSERT INTO info(idOfuser,address,connection,start) VALUES(?,?,?,?)",(ids,address,conn,times))
	

def endId(ids):
	con = lite.connect('system.db')
	times = time.time()
	with con:    
		cur = con.cursor()    
		cur.execute("UPDATE info SET end=? WHERE  idOfuser=?",(times,ids))
		
def updateAppId(ids,app):
	con = lite.connect('system.db')
	with con:    
		cur = con.cursor()    
		cur.execute("UPDATE info SET appId=? WHERE  idOfuser=?",(app,ids))
		

def updateUserName(ids,name):
	con = lite.connect('system.db')
	with con:    
		cur = con.cursor()    
		cur.execute("UPDATE info SET username=? WHERE  idOfuser=?",(name,ids))
		


def updateSecure(ids,c,s):
	con = lite.connect('system.db')
	with con:    
		cur = con.cursor()    
		cur.execute("UPDATE info SET secure=? AND ssl=?  WHERE idOfuser=?",(s,c,ids))
		

def updateExit(ids,exit):
	con = lite.connect('system.db')
	with con:    
		cur = con.cursor()    
		cur.execute("UPDATE info SET exit=? WHERE  idOfuser=?",(exit,ids))
		






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
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			ssl_sock = ssl.wrap_socket(s,
	                           ca_certs="server.crt",
	                           cert_reqs=ssl.CERT_REQUIRED)
			ssl_sock.connect(('192.168.1.21', 2030))
			deal(ssl_sock)
		except:
			print "Can't connect: "+str(sys.exc_info())
			time.sleep(5)
		






