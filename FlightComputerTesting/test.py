from config import *
import json
from packet import *

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 6969

id_mapping = {
    0:[14, 'AC1'], # PRESSURANT FLOW
    1:[17, 'AC1'], # LOX VENT
    2:[20, 'AC1'], # PROP VENT
    3:[18, 'FC'], # ARM
    4:[15, 'FC'], # LOX MAIN
    5:[19, 'FC'] # PROP MAIN
}


# Create https server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)


# create UDP sending socket
board_ips = {
    'AC1': "10.0.0.21",
    'AC2': "10.0.0.22",
    'AC3': "10.0.0.23",
    'FC': "10.0.0.42"
}
UDP_PORT = 42069

# print("UDP target IP: %s" % UDP_IP)
# print("UDP target port: %s" % UDP_PORT)
send_sock = socket.socket(socket.AF_INET, # Internet
                 socket.SOCK_DGRAM) # UDP
    

numValves = 6
valve_states = [False]*numValves


while True:    
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request_str = client_connection.recv(2048).decode()
    
    
    print(f"request_contents: \n'{request_str}'")
    
    if 'valve' in request_str:
        craft_states = request_str[request_str.index('valves=')+len('valves='):].split(',')
        craft_states = list(map(lambda x: x.lower() == 'true',craft_states))
        print(craft_states)
        for i in range(len(craft_states)):
            print(i)
            if craft_states[i] != valve_states[i]:
                new_state = craft_states[i]
                print(f"New State: {new_state}")
                valve_states[i] = new_state
                if new_state:
                    data = 1
                else:
                    data = -1
        
                id, board = id_mapping[i]
        
                print(i, id_mapping[i])
                if board:
                    pac = Packet([data],id=id)
                    print(f"message: {pac.encode_data()}")
                    send_sock.sendto(pac.encode_data().encode('utf-8'), (board_ips[board], UDP_PORT))
    print('------------------')
    
    time.sleep(1)

    # Send HTTP response
    response = f'HTTP/1.0 200 OK\n\nValve Command Received!'
    client_connection.sendall(response.encode())
    client_connection.close()

# Close socket
server_socket.close()
