import socket
import threading
import json

clock=1
messages = []
lastSentId = -1

clients = set()

clientPort = 5002
serverPort = 5000

def broadcastClints():
    global clientPort
    for address in clients:
        try:
            client_socket = socket.socket()  
            host = address # client address
            client_socket.connect((host, clientPort))   # connect to client server
            client_socket.close()
        except:
            clients.remove(address)

    print(clients)

    global lastSentId, messages
    try:
        print("boradcasting")
        if lastSentId < len(messages)  - 1:
            data = messages[lastSentId+1:]   # message content
            for address in clients:
                print(address)
                client_socket = socket.socket()  
                host = address # client address
                client_socket.connect((host, clientPort))   # connect to client server
                client_socket.send((json.dumps(data)).encode())
                client_socket.close()
            lastSentId = len (messages) - 1
    except:
        print("error occured while broadcasting")
    finally: 
        return

def receiveClient(client, address): # receive message from specific client.
    global clock
    try:
        clock = clock + 1
        client.send(str(clock).encode())
        received = client.recv(1024).decode()
        if len(received) > 0:
            timestamp,message = json.loads(received)
            messages.append([message,timestamp])
            clock = max(clock, timestamp) + 1
            print(message)
        client.close()
        threading.Thread(target=broadcastClints, args=()).start()
    except:
        print("error occured")
    finally:
        # clients.remove(address)
        return

def server_program():
    global serverPort
    host = socket.gethostname() #set local host
    server_socket = socket.socket()  
    server_socket.bind((host, serverPort))  
    server_socket.listen(100) # 100 clients set connection available
    print("Server is running...")

    while True:
        client, address = server_socket.accept() # accept client requiest
        print(address, " is connected")
        clients.add(address[0])
        threading.Thread(target=receiveClient, args=(client,address[0],)).start() #listening client socket.

if __name__ == '__main__':
    server_program()