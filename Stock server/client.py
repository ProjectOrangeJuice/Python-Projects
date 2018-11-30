import socket
import json
import sqlite3

jsonErrorMessage = json.dumps({"type":"error","data":"Incorrect json format"});
serverErrorMessage = json.dumps({"type":"error","data":"Server error"});
incorrectAuth = json.dumps({"type":"auth","data":"incorrect"})
blockedAuth = json.dumps({"type":"auth","data":"blocked"})


def clientAccept(client,address):
    try:
        print  'connection from', address

        #read the data line by line until end of stream
        #!! Socket should time out to prevent somebody from holding onto the
        # connection forever !!#

        for line in readlines(client):
            decoded = ""
            try:
                decoded = json.loads(line)
            except Exception as e:
                # Failed to decode, data sent is incorrect
                # Default failed response
                client.sendall(jsonErrorMessage)
                client.close()
                print "Error in json: ",e
                break

            if(decoded["type"]=="auth"):
                try:
                    decoded["username"]
                    decoded["password"]
                except:
                    client.sendall(jsonErrorMessage)
                try:
                    client.sendall(authUser(decoded["username"],decoded["password"]))
                    client.close()
                    break
                except Exception as e:
                    client.sendall(serverErrorMessage)
                    print "Auth error: ",e
                    client.close()
                    break



            print line
    finally:
        # Clean up the connection
        client.close()



def authUser(username,password):


    db = sqlite3.connect('data.base')
    c = db.cursor()
    c.execute('INSERT INTO keyhold(details) VALUES("abc")')
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username,password,))
    if(c.fetchone()):
        c.execute('INSERT INTO keyhold(details) VALUES("abc")')
        db.close()
        return json.dumps({"type":"auth","data":"SOMERANDOMSTUFF"})
    else:
        db.close()
        return incorrectAuth




def readlines(sock, recv_buffer=4096, delim='\n'):
	buffer = ''
	data = True
	while data:

		data = sock.recv(recv_buffer)
		buffer += data

		while buffer.find(delim) != -1:
			line, buffer = buffer.split('\n', 1)
			yield line
	return
