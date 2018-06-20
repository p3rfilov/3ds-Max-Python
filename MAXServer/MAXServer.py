import socket
from threading import Thread
try: import pymxs
except: print("pymxs module is available only in 3ds Max 2017+")

class MAXServer(Thread):
	'''
    Local TCP Server for processing Maxscript commands sent from MAXClient.
    
    Usage:
    Place MAXServer_Startup.ms and MAXServer.py in 3ds Max ..\scripts\Startup folder
    '''
	def __init__(self, host='', port=0): # dynamically assigned port
		Thread.__init__(self)
		self.host = host
		self.port = port
		self.buffer = 2048
		self.queue = 5
		self.running = False
		
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind((self.host, self.port))
		self.socket.listen(self.queue)
		self.socket.setblocking(False)
	
	def run(self):
		self.running = True
		while self.running:
			try:
				client, address = self.socket.accept()
				connected = True
			except socket.error:
				connected = False
			if connected:
				client.setblocking(True)
				command = client.recv(self.buffer).decode()
				if command:
					if command == 'stop':
						self.stop()
						result = 'Shutting down Server'
					else: 
						result = self.execute(command)
					client.sendto(result.encode(),(self.host, self.port))
				client.close()
				
	def execute(self, command):
		try:
			with pymxs.mxstoken():
				result = pymxs.runtime.execute(command)
		except:
			result = False
		return result
				
	def stop(self):
		self.running = False
		if self.socket:
			self.socket.close()

if __name__ == '__main__':
	MAXServer().start()
	