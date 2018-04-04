import psutil

class portScanner():
    def get3dsMaxPorts(self):
        ports = []
        for process in psutil.process_iter():
            if process.name() == '3dsmax.exe':
                for p in process.connections():
                    port = p.laddr.port
                    ports.append(port)
        return ports
                
if __name__ == '__main__':
    ports = portScanner().get3dsMaxPorts()
    print(ports)