import share,sys,time
import sqlite3 as lite


def connection(c,addr):
	##vars
	auth = False
	username = ""
	extra = False
	lis = False
	
	
	for line in readlines(c):
		
		##DELETE WHEN NOT REQUIRED.
		share.log("[MSG] "+line)
		
		if(not auth):
			##required login details otherwise it will ignore what ever it is
			code = line[:4]
			line = line[5:len(line)]
			if(code== "AUTH"):
				username = authenticate(c,line)
				if(username != ""):
					share.send(c,"AUTH GOOD")
					if("-" in username):
						username = username+"-lis"
						lis = True
						
					if(username in share.userlist):
						share.userlist[username].shutdown(1)
						share.userlist[username].close()
						
					share.userlist[username] = c
					auth = True
					
					continue
					
				else:
					share.send(c,"AUTH wrong")
			
			elif(code=="LOG1"):
				username = authenticate2(c,line)
				if(username != ""):
					share.send(c,"AUTH GOOD")
					if(username in share.userlist):
						share.userlist[username].shutdown(1)
						share.userlist[username].close()
						
					share.userlist[username] = c
					auth = True
					extra = True
					continue
					
				else:
					share.send(c,"AUTH wrong")
					
			else:
				share.send(c,"AUTH try")
				
		
		if(extra and auth and not lis):
			##the non upper level user access
			code=line[:4]
			line =line[5:len(line)]
			if(code=="SEND"):
				name = username.split("-")
				sender(line,name[0],name[1])
		
			elif(code =="LOGO"):
				share.clear(c,username)
				c.shutdown(1)
				c.close()
			
			else:
				share.send(c,"NFND")
		
		if(auth and not extra and lis):
			##user has logged in, access has been granted.
			code=line[:4]
			line =line[5:len(line)]
			
			
			if(code =="LOGO"):
				share.clear(c,username)
				c.shutdown(1)
				c.close()
			
			elif(code =="SEND"):
				sendlocal(c,username,line)
			
			
			
			
			
			
			else:
				share.send(c,"NFND")
		
		
		if(auth and not extra and not lis):
			##user has logged in, access has been granted.
			##this is the messenger access, the others are "extra"
			code=line[:4]
			line =line[5:len(line)]
			
			
			if(code =="LOGO"):
				share.clear(c,username)
				c.shutdown(1)
				c.close()
			
		
			elif(code=="SEND"):
				sendTo(username,c,line)
			
			elif(code=="RMSG"):
				recall(username,c)
			
			else:
				share.send(c,"NFND")
				
		


	share.log("[connection] end "+str(c))
	share.clear(c,username)






def sender(data,master,name):
	master = master+"-"+name+"-lis"
	share.log("[sender] master: "+master+" from: "+name +" with: "+data)
	msg = "SELF "+name+" "+data
	##now we need to get the connection data of the main user
	con = None
	try:
		con = share.userlist[master]
		share.send(con,msg)
	except:
		share.log("[ERROR] at sender, unable to find master in connected list - "+str(sys.exc_info()))
	
	


def sendlocal(c,username,line):
	username = username.split("-")[0]
	addressTo = line[:4]
	addressTo = addressTo.upper()
	msg = line[5:len(line)]
	addressTo = username+"-"+addressTo
	share.log("[local send] from: "+username+" to: "+addressTo+" Sending: "+msg)
	con = None
	try:
		con = share.userlist[addressTo]
		share.send(con,msg)
	except:
		##local user isn't connected.
		share.send(c,"ERRO "+addressTo+" OFF")


def authenticate(c,data):
	share.log("[AUTH] "+data)
	try:
		username,password = data.split("::")
	except:
		return ""
	username = username.upper()
	if("-" in username):
		t = username.split("-")
		ty = t[1]
		username = t[0]
	else:
		ty = ""
	password = password.rstrip()
	print "using ",username
	con = lite.connect('system.db')
	with con:    
	
		cur = con.cursor()    
		cur.execute("SELECT * FROM accounts WHERE master=? AND password=?",(username,password))
		
		rows = cur.fetchall()
		
		for row in rows:
			share.log("[AUTH] Found user!("+username+") ")
			if(ty!=""):
				return username+"-"+ty
			else:
				return username
			
	return ""



def getContacts(username,c):
	
	share.log("[CONTACTS] Finding for "+username+"...")
	
	con = lite.connect('messenger.db')
	with con:    
	
		cur = con.cursor()    
		cur.execute("SELECT * FROM contacts WHERE account=? ",(username,))
		
		rows = cur.fetchall()
		
		for row in rows:
			share.log("[CONTACTS] Found:"+row[1])
			share.send(c,"CONT "+row[1]) #online/offline. check userlist

def authenticate2(c,data):
	share.log("[AUTH non master] "+data)
	try:
		master,name,password = data.split("::")
	except:
		print "return as no enough values"
		return ""
	master = master.upper()
	name = name.upper()
	password = password.rstrip()
	con = lite.connect('system.db')
	with con:    
	
		cur = con.cursor()    
		cur.execute("SELECT * FROM extra WHERE master=? AND name=? AND pin=?",(master,name,password))
		
		rows = cur.fetchall()
		
		for row in rows:
			share.log("[AUTH] Found user!(["+master+"] "+name+")")
			r = master+"-"+name
			return r
			
	return ""





def sendTo(sender,c,line):
	sendTo = line[:4].upper()
	message = line[5:len(line)]
	share.log("[CHECK] user exist: "+sendTo)
	#check the user exists.
	exist = False
	con = lite.connect('system.db')
	with con:    
	
		cur = con.cursor()    
		cur.execute("SELECT * FROM accounts WHERE master=?",(sendTo,))
		
		rows = cur.fetchall()
		
		for row in rows:
			exist = True
			
		
	if(exist):
		share.log("[SENDTO] User did exist, trying to send..")
		try:
			connection = share.userlist[sendTo]
			m = "MSG! "+sender+" "+message
			share.send(connection,m)
		except:
			share.log("[SENDTO] FAILED, user wasn't online - "+str((sys.exc_info())))
			#as the user wasnt there, we'll add it to the database for them to collect later.
			con = lite.connect('messenger.db')
	
			with con:    
			
				cur = con.cursor()    
				t = time.strftime("%d/%m %H:%M:%S")
				cur.execute("INSERT INTO messages(account,sender,time,message,delivered) VALUES(?,?,?,?,?)",(sendTo,sender,t,message,"False"))
				share.log("[DELAY] Message added to database for "+sendTo+" Sent by "+sender)
				share.send(c,"MSG! JUGGERNAUT user isn't online, message will be held for "+sendTo)
	else:
		share.send(c,"MSG! JUGGERNAUT The user "+sendTo+" doesn't exist")
				
			
		
def recall(username,c):
	share.log("[RECALL] Finding messages for "+username+"...")
	
	con = lite.connect('messenger.db')
	with con:    
	
		cur = con.cursor()    
		cur.execute("SELECT * FROM messages WHERE account=? AND delivered=? ",(username,"False"))
		
		rows = cur.fetchall()
		
		for row in rows:
			share.log("[MESSAGE] Found:"+str(row[5]))
			msg = "RMSG "+row[1]+" "+row[2]+" "+row[3]
			share.send(c,msg) 
			cur.execute("UPDATE messages SET delivered=? WHERE id=?", ("True", row[5]))        
			con.commit()
		share.send(c,"RMSG over")


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
			share.log("[ERROR] Connection closed without warning!")
			return 

	return
