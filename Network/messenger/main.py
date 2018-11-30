import socket, ssl, time,sys


import sqlite3 as lite



#################################
#		messenger server		#
################################
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = ssl.wrap_socket(s,
	ca_certs="server.crt",
	cert_reqs=ssl.CERT_REQUIRED)

def deal(c):
	
	print "on deal"
	c.send("AUTH JUGN-MSGS_pass\n")
	
	for line in readlines(c):
		print "line is: ",line
		code = line[:4]
		line = line[5:len(line)]
		
		if(code=="SEND"):
			print "send code, using line of ",line
			e = line.split(" ")
			if(e[0]=="success"):
				print "success for ",e[1]
				success(e[1])
			if(e[0]=="fail"):
				print "failed for ",e[1]
				failed(e[1])
		
		
		elif(code=="MSGS"):
			
			co = line.split("_")[1][:4]
			if(co=="SEND"):
				sender(line)
			
			elif(co=="PAST"):
				past(line)
	
	

def past(line):
	print "past line: ",line
	try:
		t = line.split("_",1)
		userFrom = t[0]
		line = t[1][5:len(t[1])]
		line = line.split("_",1)
		print line
	except:
		print str(sys.exc_info())
		return
	print "LINE ARE THING: 2",line
	MID = line[0]
	con = lite.connect('hold.db')
	if(MID == "0"):
		print "0!!"
		with con:    
			cur = con.cursor()    
			cur.execute("SELECT * FROM messages WHERE userTo=? OR fromName=?",(userFrom ,userFrom ))
			rows = cur.fetchall()

			for row in rows:
				print "row: ",row
				ssl_sock.send("SEND "+userFrom+"_000_PAST "+row[0]+"_"+row[3]+"_"+row[2]+"_"+row[4]+"\n")
				##update sent
	else:
		with con:    
			cur = con.cursor()    
			cur.execute("SELECT * FROM messages WHERE userTo=? OR fromName=?",(userFrom ,userFrom ))
			rows = cur.fetchall()

			for row in rows:
				print "row: ",row
				if(float(MID) > float(row[2])):
					ssl_sock.send("SEND "+userFrom+"_000_PAST "+row[0]+"_"+row[3]+"_"+row[2]+"_"+row[4]+"\n")
					##update sent
	
	

		
		
	

def success(MID):
	##we'll update the database that it's sent.
	con = lite.connect('hold.db')
	with con:    
		cur = con.cursor()    
		cur.execute("UPDATE messages SET sent=? WHERE  MID=?",("yes",MID))
		cur.execute("SELECT * FROM messages WHERE MID=? ",(MID,))
		rows = cur.fetchall()
		for row in rows:
			ssl_sock.send("SEND "+row[0]+"_000_SENT_"+row[1]+"_"+MID+"\n")
		
def failed(MID):
	con = lite.connect('hold.db')
	with con:    
		cur = con.cursor()    
		cur.execute("SELECT * FROM messages WHERE MID=? ",(MID,))
		rows = cur.fetchall()
		for row in rows:
			ssl_sock.send("SEND "+row[0]+"_000_STOR_"+row[1]+"_"+MID+"\n")

def sender(line):
	print "sender line: ",line
	try:
		t = line.split("_",1)
		userFrom = t[0]
		line = t[1][5:len(t[1])]
		line = line.split("_",2)
	#	line[3]
	
	except:
		print str(sys.exc_info())
		return
	
	msgid = line[0]
	username = line[1]
	message = line[2]
	if(len(username) < 9 or len(username) > 10):
		print "username incorrect"
		return
	#add the message
	#juggernaut will reply with some information.
	# does the user exist
	# did they get the message
	
	MID= time.time()
	con = lite.connect('hold.db')
	with con:    
		cur = con.cursor()    
		cur.execute("INSERT INTO messages(fromName,fromId,MID,userTo,message) VALUES(?,?,?,?,?)",(userFrom,msgid,str(MID),username,message))
		print "added now sending with MID of ",MID
		ssl_sock.send("SEND "+username+"_"+str(MID)+"_NEW!_"+userFrom+"_"+str(MID)+"_"+message+"\n")
	











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
		ssl_sock = ssl.wrap_socket(s,
                           ca_certs="server.crt",
                           cert_reqs=ssl.CERT_REQUIRED)
		ssl_sock.connect(('192.168.1.19', 2030))
		deal(ssl_sock)
		#except:
		#	print "Can't connect: "+str(sys.exc_info())
		#	time.sleep(5)
		






