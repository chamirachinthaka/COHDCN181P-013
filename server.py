import socket,sys
from threading import Thread

def sent():
	while True:
		msg_for_client = raw_input("Server :")
		conn_obj.send(msg_for_client)
		
		if not msg_for_client:
			break
	
if __name__ == '__main__':
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	host_name = socket.gethostname() #To get the name of host
	port_number = 8888
	print "The name of local machine",host_name

	host_port_pair = (host_name,port_number)
	print host_port_pair
	sock.bind(host_port_pair) #Bind address to the socket

	sock.listen(1)
	conn_obj,addr = sock.accept()
	print "Got a connection from ",addr

	#t1 = Thread(target=recev, args=())
	#t1.deamon = True
	#t1.start()
	t2 = Thread(target=sent, args=())
	t2.deamon = True
	t2.start()

	while True:
		try:
			msg_from_client = conn_obj.recv(1024)
			print "\nClient :", msg_from_client
		except KeyboardInterrupt:
			conn_obj.close()
			sys.exit()

		if not msg_from_client:
			break
