import socket
import thread
#myfiles
import client

def main(host,port):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    server_address = (host, port)
    print  'started on %s port %s' % server_address
    sock.bind(server_address)
    #listen for incoming connections
    sock.listen(1)

    while True:#need connection to end
        connection,address = sock.accept()
        thread.start_new_thread( client.clientAccept, (connection,address, ) )



if __name__ == '__main__':
    main("localhost",10101)
