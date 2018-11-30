#main
import share,sys,time,random,string,tasks,ssl
import sqlite3 as lite
import base64


def connection(c,addr,ids):
	try:
		#c.settimeout(600.0)
		try:
			c = ssl.wrap_socket(c,
					server_side=True,
					certfile="server.crt",
					keyfile="server.key")
			share.updateSecure(ids,c,"Yes")
			share.MupdateSecure(ids,c)
		except:
			share.log("[ERROR SSL] "+str(sys.exc_info()))
			share.send(c,ids,"SSL OFF")
	
		
		
		auth = False
		username = None
		goes = 0
		app = "0000"
		share.connections[ids] = c
		
		for line in readlines(c):
			print "line: ",line
			##encryption block here
			
			##
			
			try:
				code = line[:4].upper()
				line = line[5:len(line)]
				line = line.rstrip()
			except:
				share.log("[Error] APPID_"+ids+" not enough values (needs two)")
		
		
			if(code=="DISP"):
				print share.userlist#working
				print share.connections #not working..
				print share.num # working
		
			if(code == "APP!"):
				print "App id"
				if(tasks.checkAppId(line,ids,c)):
					app=line
					
				else:
					share.send(c,ids,"APP! fail")
			if(code=="LOGT"):
					share.log("[LOGT] "+ids)
					break
		
			elif(not auth):
				#they need to login.
				if(len(line)>5):
					username = tasks.authenticate(c,line,app,ids)
					if(username == "OVERMAX"):
						#too many logins.. What do we want to do about that?
						print "Undecided what to do, but over max."
					if(username != ""):
						#correct
						share.send(c,ids,"AUTH correct")
						share.userlist[username+ids]=c
						share.updateUserName(ids,username)
						auth = True
						share.MupdateUser(ids,username)
						if(username[:4]=="MONI"):
							share.giveList()
						
					else:
						share.send(c,ids,"AUTH wrong")
						goes = goes + 1
						print "Goes: ",goes
						if(goes>3):
							
							share.block(addr,"Wrong username/password")
							break
						
		
		
			if(auth):
				#they've logged in
				
				if(code=="SEND"):
					#try:
					tasks.send(c,ids,line,username)
					#except:
					#	share.log("[ERROR] "+str(sys.exc_info()))
					#	share.send(c,ids,"SEND didn't work")
				elif(code=="CODE"):
					#generate a token code.
					if(app=="0000"):
						share.send(c,ids,"CODE app id needed")
					else:
						token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(300))
						tasks.updateToken(token,username,app,ids)
						share.send(c,ids,"CODE "+token)
				elif(code=="PASS"):
					tasks.changePassword(ids,username,c,line)
				elif(code=="AUTH"):
					share.send(c,ids,"AUTH DONE")
		
		#do the disconnect stuff...
		
		share.clear(username,c,ids)
		share.MdelC(ids)
				
	except:
		print "Major error has caused the connection is fall.. "
		share.log("[error] "+str(sys.exc_info()))
		share.clear(username,c,ids)
		share.MdelC(ids)
		
	
	




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
