import socket,sys
from threading import Thread
		
def sen():
	while True:
		msg_for_server = raw_input("Client : ")
		sock.send(msg_for_server)
		
		if not msg_for_server:
				break		

if __name__ == '__main__':
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	host_name = socket.gethostname() #To get the name of host
	port_number = 8888

	host_port_pair = (host_name,port_number) #A tuple

	sock.connect(host_port_pair)  #To actively intiate the TCP Server connection

	t1 = Thread(target=sen, args=())
	t1.deamon = True
	t1.start()
	
	#t2 = Thread(target=rec, args=())
	#t2.deamon = True
	#t2.start()

	while True:
		try:
			msg_from_server = sock.recv(1024)
			print "\nServer :",msg_from_server
		except KeyboardInterrupt:
			sys.exit()

		if not msg_from_server:
				break
		
