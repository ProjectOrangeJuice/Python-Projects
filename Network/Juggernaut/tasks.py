#tasks
import share,sys,time,random,string
import sqlite3 as lite
import base64





def checkAppId(theId,ids,c):
	con = lite.connect('system.db')
	with con:    
	
		cur = con.cursor()    
		cur.execute("SELECT * FROM app WHERE id=?",(theId,))
		
		rows = cur.fetchall()
		
		for row in rows:
			#app id is allowed
			share.updateAppId(ids,theId)
			share.Mapp(row[1],ids)
			return True
		return False



def changePassword(ids,username,c,line):
	share.log("[pass change] trying for: "+ids)
	try:
		pa = line.split("_",1)
	except:
		#wrong already.
		share.send(c,ids,"PASS fail")
		return
	
	con = lite.connect('system.db')
	with con:    
		print "Passwords: ",pa
		
		cur = con.cursor()    
		cur.execute("SELECT * FROM accounts WHERE username=? AND password=?",(username[:4],pa[0]))
		
		rows = cur.fetchall()
		if(not rows):
			share.send(c,ids,"PASS fail")
		else:
			cur.execute("UPDATE accounts SET password=? WHERE  username=?",(username[:4],pa[1]))
			share.send(c,ids,"PASS success")
			cur.execute("DELETE FROM token WHERE account=? ",(username,))
			share.clear(username,c,ids)
			share.MdelC(ids)
		
	



def send(c,ids,msg,username):
	share.log("[send] from:"+ids+" with: "+msg)
	msg = msg.split("_",2)
	print "msg values: ",msg
		
	allow = share.checkAllow(msg[0],username)
	#allow = True
	if(allow):
		print "allowed"
		f = False
		for c2 in share.findEach(msg[0]):
			print "find each.."
			f = True
			share.send(c2,ids,"MSGS "+username+"_"+msg[2])
		if(f):
			share.send(c,ids,"SEND success "+msg[1])
		else:
			share.send(c,ids,"SEND fail "+msg[1])
			
	if(allow == "NO"):
		#share.send(c,ids,"SEND "+msg[0]+" doesn't exist")
		print "{doesn't exist}"
	if(not allow):
		share.send(c,ids,"SEND rejected "+msg[1])
		

def updateToken(token,username,app,ids):
	
	con = lite.connect('system.db')
	
	with con:    
		cur = con.cursor()    
		cur.execute("INSERT INTO token(account,code,app) VALUES(?,?,?)",(username,token,app))
		share.log("[TOKEN] new for "+ids+" with app "+app)


def authenticate(c,data,app,ids):
	con = lite.connect('system.db')
	share.log("[AUTH] "+ids)
	try:
		username,password = data.split("_")
	except:
		return ""
	#try:
	#	password = base64.b64decode(password)
	#	print "base64 worked :",password
	#except:
	#	print "base64 failed on: ",password
	print "the app id is: ",app
		
	username = username.upper()
	try:
		u1 = username[:4]
		u2 = username[5:9]
		
	except:
		return ""
	password = password.rstrip()
	
	with con:    
	
		cur = con.cursor()    
		cur.execute("SELECT * FROM accounts WHERE username=? AND password=?",(u1,password))
		
		rows = cur.fetchall()
		if(not rows):
			share.log("[AUTH] not found, trying token login for "+ids)
			cur.execute("SELECT * FROM token WHERE account=? AND code=? AND app=?",(username,password,app))
		
			rows = cur.fetchall()
		
		
		for row in rows:
			share.log("[AUTH] Found user!("+u1+")")
			
			cur2 = con.cursor()    
			cur2.execute("SELECT * FROM other WHERE name=? ",(u2,))
		
			rows2 = cur2.fetchall()
			for row2 in rows2:
				##logged in!
				
				try:
					share.log("[AUTH] "+username+" has "+str(share.num[username])+" current connections.")
				except:
					share.log("[AUTH] users first connection")
				try:
					if(int(share.num[username])>2):
						share.log("[AUTH] "+username+" overmax")
						return "OVERMAX"
					else:
						
						share.num[username] = share.num[username] + 1
						return username
						
				except:
					share.num[username] = 1
					return username
		
			
	return ""
