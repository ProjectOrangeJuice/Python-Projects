#share

import sys,time,datetime,ssl,decimal
import sqlite3 as lite

num={} #number of connections the user has
userlist = {} #username:connection
connections= {} # every connection linked to the ID


def log(text):
	with open("log.txt", "a") as myfile:
		t = time.strftime("%d/%m %H:%M:%S")
		myfile.write("{"+t+"} "+text+"\n")
		print "{"+t+"} "+text


def send(c,ids,msg):
	log("[SEND] to "+ids+": "+msg)
	try:
		c.send(msg+"\n")
	except:
		log("[ERROR] Could not send, clear lists of "+ids)
		


def addNewId(address,conn,ids,times):
	con = lite.connect('system.db')
	
	with con:    
		cur = con.cursor()    
		cur.execute("INSERT INTO info(idOfuser,address,connection,start) VALUES(?,?,?,?)",(ids,address,conn,times))
		log("[connection] Client connected "+ids)

def endId(ids):
	con = lite.connect('system.db')
	times = time.time()
	with con:    
		cur = con.cursor()    
		cur.execute("UPDATE info SET end=? WHERE  idOfuser=?",(times,ids))
		log("[connection] Client ended "+ids)

def updateAppId(ids,app):
	con = lite.connect('system.db')
	with con:    
		cur = con.cursor()    
		cur.execute("UPDATE info SET appId=? WHERE  idOfuser=?",(app,ids))
		log("[connection] Client "+ids+" appId updated with:"+app)

def updateUserName(ids,name):
	con = lite.connect('system.db')
	with con:    
		cur = con.cursor()    
		cur.execute("UPDATE info SET username=? WHERE  idOfuser=?",(name,ids))
		log("[connection] Client "+ids+" username updated with:"+name)


def updateSecure(ids,c,s):
	con = lite.connect('system.db')
	with con:    
		cur = con.cursor()    
		cur.execute("UPDATE info SET secure=? AND ssl=?  WHERE idOfuser=?",(s,str(c),ids))
		log("[connection] Client "+ids+" secure updated with:"+s)

def updateExit(ids,exit):
	con = lite.connect('system.db')
	with con:    
		cur = con.cursor()    
		cur.execute("UPDATE info SET exit=? WHERE  idOfuser=?",(exit,ids))
		log("[connection] Client "+ids+" exit updated with:"+exit)


def findEach(name):
	for value,con in userlist.iteritems():
		
		v = value[:9]

		if(v == name):
			
			yield con
	return



def block(ip,reason):
	con = lite.connect('system.db')
	times = time.time()
	with con:    
		cur = con.cursor()    
		cur.execute("INSERT INTO system(block,time,reason) VALUES(?,?,?)",(ip,times,reason))
		log("[connection] added block for "+ip +" Reason: "+reason)

def unblock(ip):
	con = lite.connect('system.db')
	with con:    
		cur = con.cursor()    
		cur.execute("UPDATE system SET active='False' WHERE  block=?",(ip,))
		log("[connection] unblocked: "+ip)

def checkBlock(ip):
	con = lite.connect('system.db')
	with con:    
		cur = con.cursor()    
		cur.execute("SELECT * FROM system where block=? ORDER BY time DESC",(ip,))
		
		for row in cur:
			newt = time.time()#float(row[1])
			print "newt ",float(newt)
			print "other ",float(row[1])+600
			
			if( float(newt) >float(row[1])+600):
				print "not blocked"
				return "Free"
			else:
				return "Blocked"
		return "Free"

def clear(username,c,ids):
	endId(ids)
	log("[clear] "+ids)
	try:
		#c.shutdown(1)
		c.close()
	except:
		updateExit(ids,"Unclean exit.")
	
	try:
		connections.pop(ids,None)
	except:
		print "error clearing "+str(sys.exc_info())
		return 
	if(username != None or username != ""):
		
		try:
			userlist.pop(username+ids,None)
			num[username] = num[username]-1
		except:
			print "error clear "+str(sys.exc_info())
			print "list of the users.."
			print userlist
			return



def checkAllow(username,sender):
	con = lite.connect('system.db')
	try:
		username = username.split("-")
		username[1]
	except:
		return False
	with con:    
		cur = con.cursor()    
		cur.execute("SELECT * FROM other where account=? and name=?",(username[0],username[1],))
		
		for row in cur:
			if(sender in row[2] or row[2] == "ALL"):
				print "Sender in list, allowed ("+row[2]+")"
				return True
			else:
				return False
		return "NO"




















########################################################################
#		monitor updates are kept here  								   #
########################################################################


def giveList():
	t = None
	t2 = None
	t3 = None
	for name,number in num.iteritems():
		if(t==None):
			t=name+"::"+str(number)
		t = t+";"+name+"::"+str(number)
	for username,connection in userlist.iteritems():
		if(t2==None):
			t2=username+"::"+str(connection)
		t2 = t2+";"+username+"::"+str(connection)
	for theId,connection in connections.iteritems():
		if(t3==None):
			t3=theId+"::"+str(connection)
		t3 = t3+";"+theId+"::"+str(connection)
	
	for c in findEach("MONI-INFO"):

		c.send("LIST "+t+"_"+t2+"_"+t3+"\n") 

def MaddC(ids,c,address):
	
	try:
		for c in findEach("MONI-INFO"):
			c.send("NEW! "+ids+"_"+str(address)+"_"+str(c)+"\n")
	except:
		print "connect monitor.."
		print str(sys.exc_info())
def MdelC(ids):
	
	try:
		for c in findEach("MONI-INFO"):
			c.send("DEL! "+ids+"\n")
	except:
		print "connect monitor.."
		print str(sys.exc_info())
		
def Mapp(app,ids):
	try:
		for c in findEach("MONI-INFO"):
			c.send("APP! "+ids+"_"+app+"\n")
	except:
		print "connect monitor.."
		print str(sys.exc_info())


def MupdateUser(ids,name):
	
	try:
		for c in findEach("MONI-INFO"):
			c.send("USER "+ids+"_"+name+"\n")
	except:
		print "connect monitor.."
		print str(sys.exc_info())
def MupdateSecure(ids,c):
	try:
		for c in findEach("MONI-INFO"):
			c.send("SECR "+ids+"_"+str(c)+"\n")
	except:
		print "connect monitor.."
		print str(sys.exc_info())
