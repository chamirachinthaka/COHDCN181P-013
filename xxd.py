import sys
import os
import re

if len(sys.argv)==2:
	filename = sys.argv[1]

if not os.path.isfile(filename):
	print'[-]'+filename+'does not exist'
	exit(0)

if not os.access(filename,os.R_OK):
	print '[-]' + filename + 'access denied'
	exit(0)

print '[-] Reading Charactors for Convert to Hexadecimal From : ' + filename
Nset = 0
with open(filename) as f:
	while True:
		j = 0
		k = 2
		tx = f.read(16)
		if len(tx) == 0:
			break

		MM = str(tx)
		MM = ''.join([i if ord(i)< 128 and ord(i)>32 else '.' for i in MM])
		
		op = "{:08x}".format(Nset)+": "
		while j<=(len(tx)-2) and k<=(len(tx)):
			op +=''.join("{:02x}".format(ord(c)) for c in tx[j:k])
			op += ' '
			j += 2
			k += 2

		
		if len(tx) % 16 != 0:
			op += "   "*(14-len(tx))+ ' ' + MM
		else:
			op += " " + MM
		
		print op
		Nset += 16
