import socket,thread,sys,time,ssl

import main,share,random,string,time


host = "192.168.1.19"   #ip of juggernaut
port = 2030	#port to connect to




try:
	s = socket.socket()
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	s.bind((host,port))
	share.log("[info] Ready for connections")
	s.listen(5)
	while(True):
		print "waiting.."
		c,addr = s.accept()
		
		
		address = addr[0]
		
		
		if(share.checkBlock(address)=="Blocked"):
			share.log("[connection] blocked for "+address)
			c.send("Blocked")
			c.shutdown(1)
			c.close()
			continue
			
		
		
		
	
		
		ids = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
		times = time.time()
		share.addNewId(str(address),str(c),ids,times)
		
		share.MaddC(ids,c,address)
		


		
		
			
		
		
		thread.start_new_thread(main.connection,(c,address,ids,))
	print "!!!!!!!!!**************************!!!!!!!!!!!!!!!!!!"

except:
	share.log("[error] "+str(sys.exc_info()))

