import socket

class WifiUDP():
    HOST = '192.168.4.255'   # Endereco IP do Servidor
    PORT = 333             # Porta que o Servidor esta
    udp  = None
    isConneted = False
    def __init__(self):
        try:
            self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.dest = (self.HOST, self.PORT)
            self.udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        except socket.error, msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]

    def connect(self):
        if self.isConneted is not True:
            try:
                self.udp.connect(self.dest)
                self.isConneted = True
            except socket.error, msg:
                print 'Failed to connect. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
                self.isConneted = False


    def send_data(self,msg):
        if self.isConneted:
            data = str.encode(msg)
            try:
                self.udp.send(data)
                return True
            except socket.error, msg:
                print 'Failed to send. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
                self.isConneted = False
                return False
        else:
            return False

my_socket = WifiUDP()
