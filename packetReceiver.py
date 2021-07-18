import sys
sys.path.append(".")

import socket 
import packet_gen

class packetReceiver:
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
    def __init__(self, host= None, port = None):
        if host != None:
            self.HOST = host
        if port != None:
            self.PORT = port   

    def receive(self):        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(data)
    def main(self):
        self.receive()

if __name__ == "__main__":
    z = packetReceiver()    
    z.main()
