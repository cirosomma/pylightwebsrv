class manageRequest:
	def __init__(self, data,client,index,directory,log):
		self.data = data
		self.client = client
		self.index = index
		self.directory = directory
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
				request[1] = '/'+self.index
			
			with open(self.directory + request[1][1:]) as x:
				self.data = x.read()
				x.close()
					
		except IOError:
			self.data = '404: Not Found'
