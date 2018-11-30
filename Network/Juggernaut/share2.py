## shared vars and functions


import sys,time


userlist = {}
connections= []


def log(text):
	with open("log.txt", "a") as myfile:
		t = time.strftime("%d/%m %H:%M:%S")
		myfile.write("{"+t+"} "+text+"\n")
		print "{"+t+"} "+text



def send(c,msg):
	log("[SEND] to "+str(c)+": "+msg)
	try:
		c.send(msg+"\n")
	except:
		log("[ERROR] Could not send, clear lists of this user!")
		

def clear(c,u):
	log("[lists]\n {connections}\n"+str(connections)+"\n{users}\n"+str(userlist))
	try:
		connections.remove(c)
	except:
		print "1",sys.exc_info()
	if(u != ""):
		try:
			userlist.pop(u,None)
		except:
			print "3",sys.exc_info()	
	log("***DELETED USER****\n[lists]\n {connections}\n"+str(connections)+"\n{users}\n"+str(userlist))
