import socket
import psutil

class MAXClient():
    '''
    Local TCP Client for sending Maxscript commands to 3ds Max.
    
    Usage:
    client = MAXClient()
    activeScenes = client.getActiveScenes()
    for port, file in activeScenes.items():
        command = 'maxFileName' #Maxscript command
        response = client.sendTo(file, command)
        print(response)
    '''
    def __init__(self, host=socket.gethostname()):
        self.host = host
        self.buffer = 2048
    
    def getActiveScenes(self):
        activeScenes = {}
        allPorts = self.get3dsMaxPorts()
        for port in allPorts:
            maxFile = self.getFileName(port)
            if maxFile:
                activeScenes[port] = maxFile
            else:
                self.attemptShutDown(port)
        return activeScenes
        
    def get3dsMaxPorts(self):
        ports = []
        for process in psutil.process_iter():
            if process.name() == '3dsmax.exe':
                for p in process.connections():
                    if p.status == 'LISTEN':
                        ports.append(p.laddr.port)
        return ports
    
    def getFileName(self, port):
        file = self.send(port, 'maxFilePath + maxFileName')
        return file
    
    def sendTo(self, filePath, command):
        sent = False
        activeScenes = self.getActiveScenes()
        for port, name in activeScenes.items():
            if name == filePath:
                self.send(port, command)
                sent = True
        if not sent:
            print('Scene not found!')
        
    def send(self, port, command):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, port))
            self.socket.sendto(command.encode(),(self.host, port))
            result = self.socket.recv(self.buffer).decode()
            if not result:
                self.attemptShutDown(port)
        except:
#             print ('Connection failed! Please make sure MAXServer is running.')
            result = False
        if self.socket:
            self.socket.close()
        return result
    
    def attemptShutDown(self, port):
        result = self.send(port, 'stop')
        print('Server:',result)
        return result
        
if __name__ == '__main__':
    client = MAXClient()
    activeScenes = client.getActiveScenes()
    for port, file in activeScenes.items():
        client.attemptShutDown(port)
