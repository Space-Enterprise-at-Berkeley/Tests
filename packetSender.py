import sys


sys.path.append(".")

import socket
import packet_gen

class packetSender:
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
    def __init__(self, host= None, port = None):
        if host != None:
            self.HOST = host
        if port != None:
            self.PORT = port        

    '''
    def fletcher16(self, message):
        sum1 = 0
        sum2 = 0
        # converts string into an array of bytes for easy math
        for byte in message.encode('ascii'):
            sum1 = (byte + sum1) % 255
            sum2 = (sum1 + sum2) % 255
        return "{:04X}".format(sum2 << 8 | sum1)

    def encode_packet(self, message):
        
       # message = id,datum,datum,datum....

        checksum = fletcher16(message)
        return "{" + message + "|" + checksum + "}"

    '''

    

    def sendPacket(self, data, id= None):
        toSend = packet_gen.Packet("SEB", 15)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(self.HOST, self.PORT)
            s.connect((self.HOST, self.PORT))
            s.sendall(bytes(toSend.encoded_message, "utf-8"))
            data = s.recv(1024)

        print('Received', repr(data))

    def main(self):
        self.sendPacket("SEB")


if __name__ == "__main__":
    z= packetSender()
    z.main()