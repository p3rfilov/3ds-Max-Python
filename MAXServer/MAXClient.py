import socket

class MAXClient():
    def __init__(self, host=socket.gethostname(), port=1984):
        self.host = host
        self.port = port
        self.buffer = 2048
        
    def send(self, command):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, self.port))
            self.socket.sendto(command.encode(),(self.host, self.port))
            result = self.socket.recv(self.buffer).decode()
        except:
            print ('Connection failed! Please make sure MAXServer is running.')
            result = False
        if self.socket:
            self.socket.close()
        return result
        
if __name__ == '__main__':
    result = MAXClient().send(' "Message sent!" ')
    print ('Server:', result)
    result = MAXClient().send('stop')
    print ('Server:', result)
