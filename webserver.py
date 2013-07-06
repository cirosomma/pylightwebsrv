#!/usr/bin/env python

import select
import socket
import sys
host = None
port = None
log = 0
directory = 'html/'
index = 'index.html'
class manageRequest:
	def __init__(self, data,client):
		self.data = data
		self.client = client
		self.createRequest()
		if log == 1:
			try:
				with open('log','a+') as f:
					f.write(client[0]+" "+data)
					f.close()
			except IOError:
				print "Doesn't can it write on log file"
	def output(self):
		return self.data
	def createRequest(self):
		request = self.data.split(" ")
		try:
			if request[1] == '/':
				request[1] = '/'+index
			
			with open(directory + request[1][1:]) as x:
				self.data = x.read()
				x.close()
					
		except IOError:
			self.data = '404: Not Found'
try:
	with open('config','r') as config:
		for line in config:
			line = line[:-1]
			newline = line.split(' : ')
			if newline[0] == 'hostname':
				host = newline[1]
			if newline[0] == 'port':
				port = int(newline[1])
			if newline[0] == 'log':
				log = int(newline[1])
			if newline[0] == 'dir':
				directory = newline[1]
			if newline[0] == 'index':
				index = newline[1]
		print 'Config data loaded'
except IOError:
	print 'Config file not found'
if(len(sys.argv) == 2 and sys.argv[1] == '-h'):
	print """Simple HTTP Server
[+] Use webserver.py <hostname> <port> or
   webserver.py <hostname>
   Can you use it without parameters but 
   hostname will be localhost.
   Can you use a simple file config.
   Ex: hostname : localhost
   port : 80
   log : 0 or 1 ( false or true)
"""
	sys.exit(1)

if (host == None and len(sys.argv) > 1):
	host = sys.argv[1]
elif host == None:
	host = 'localhost'
if (port == None and len(sys.argv) < 3):
	while 1:
		try:
			x = int(raw_input("Insert port :"))
			break
		except ValueError:
			continue

	port = x
elif port == None:
	try:
		port = int(sys.argv[2])
	except ValueError:
		print 'Port must be an integer'
		sys.exit(1)

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
	s.bind((host,port))
except socket.error:
	print 'Use command sudo for default ports'
	sys.exit(1)
s.listen(5)

while 1:
	conn, addr = s.accept()
	data = conn.recv(4096)
	if not data : break
	datas = data.split("\n")
	request = manageRequest(datas[0],addr)
	conn.send(request.output())
	conn.close()
s.close()

