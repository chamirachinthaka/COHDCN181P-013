import struct,socket,time,sys

seq_num = 0
ICMP_ECHO_REQUEST = 8

ICMP_CONTROL_MESSAGE = \
    {0: {0: 'Echo Reply',
        },
     3: {0: 'Net Unreachable',
         1: 'Destination Host Unreachable',
         2: 'Destination protocol unreachable',
         3: 'Destination port unreachable',
         4: 'Fragmentation required, and DF flag set',
         5: 'Source route failed',
         6: 'Destination network unknown',
         7: 'Destination host unknown',
         8: 'Source host isolated',
         9: 'Network administratively prohibited',
         10: 'Host administratively prohibited',
         11: 'Network unreachable for TOS',
         12: 'Host unreachable for TOS',
         13: 'Communication administratively prohibited',
         14: 'Host Precedence Violation',
         15: 'Precedence cutoff in effect',
        },
     4: {0: 'Source quench',
        },
     5: {0: 'Redirect Datagram for the Network',
         1: 'Redirect Datagram for the Host',
         2: 'Redirect Datagram for the TOS & network',
         3: 'Redirect Datagram for the TOS & host',
        },
     8: {0: 'Echo request',
        },
     9: {0: 'Router Advertisement',
        },
     10: {0: 'Router discovery/selection/solicitation',
         },
     11: {0: 'TTL expired in transit',
          1: 'Fragment reassembly time exceeded',
         },
     12: {0: 'Pointer indicates the error',
          1: 'Missing a required option',
          2: 'Bad length',
         },
     13: {0: 'Timestamp',
         },
     14: {0: 'Timestamp reply',
         },
    }


def Mass(type,code):

	AAA = ICMP_CONTROL_MESSAGE[type]
	BBB = AAA[code]
	print BBB

def recv():

	try:
		sock.settimeout(2)
		recPacket,addr= sock.recvfrom(1024)
       		current_time = time.time()
		
		ipHeader = recPacket[:20]
        	icmpHeader = recPacket[20:28]

		ver, ttl, proto, chk, src, drc = struct.unpack('!B 7x B B H 4s 4s', ipHeader)
		type, code, checksum, ID, sequence = struct.unpack("!bbHHh", icmpHeader)

		rtt =  current_time - send_time
        	#rtt *= 1000
		#rtt = round(rtt,3)
		n_rtt=((current_time - send_time)*1000)
		#print(n_rtt, current_time, send_time)
		#print type
		#print code
		if (type==0 & code==0):
			print "%d bytes from %s:  icmp_seq=%u  TTL = %u  Time=%.3f ms" % (len(icmpHeader),dest_addr , seq_num, ttl, n_rtt)

		else:
			Mass(type,code)   	

	except socket.timeout:
				
		print("Request Time Out")


def checksum(source_string):
	sum = 0
    	countTo = (len(source_string)/2)*2
    	count = 0
    	while count<countTo:
        	thisVal = ord(source_string[count + 1])*256 + ord(source_string[count])
        	sum = sum + thisVal
        	sum = sum & 0xffffffff # Necessary?
       		count = count + 2
 
    	if countTo<len(source_string):
        	sum = sum + ord(source_string[len(source_string) - 1])
        	sum = sum & 0xffffffff # Necessary?
 
    	sum = (sum >> 16)  +  (sum & 0xffff)
    	sum = sum + (sum >> 16)
    	answer = ~sum
    	answer = answer & 0xffff
 
    # Swap bytes. Bugger me if I know why.
    	answer = answer >> 8 | (answer << 8 & 0xff00)
 
    	return answer

if __name__ == '__main__':
	addr = raw_input("Enter Destination Address : ")
	print "ping %s..." % addr

	icmp = socket.getprotobyname("icmp")
	sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,icmp)
	
	dest_addr  =  socket.gethostbyname(addr)

	while (seq_num<4):
    ## create ping packet 
        	seq_num += 1
		
		my_checksum = 0
		header = struct.pack("bbHh", ICMP_ECHO_REQUEST, 0, my_checksum, 1)
		
		bytesInDouble = struct.calcsize("d")
		data = (192 - bytesInDouble) * "Q"
		data = struct.pack("d", time.time()) + data
        	
		my_checksum = checksum(header+data)
		header2= struct.pack("bbHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), 1)
		
		Packet = header2+ data
    		
    		sock.sendto(Packet, (dest_addr, 1))
		send_time=time.time()
		
		recv()

sys.exit()


		
        		
	
