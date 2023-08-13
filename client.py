import socket
import time
import sys
import json
import threading
clock = 1
serverIp=socket.gethostname()

def receive_messages():
    port = 5002  
    server_socket = socket.socket()  
    server_socket.bind((serverIp, port))  
    server_socket.listen(1)
    while True:
        client, _ = server_socket.accept()
        received = client.recv(1024)
        if len(received) > 0 :
            messages = json.loads(received)
            with open('readme.txt', 'a') as f:
                for message in messages:
                    f.write("message: "+ message[0] + "\n")
                    f.write("timestamp: " + str(message[1]) + "\n")
        client.close()

def client_program(message):
    global clock
    try:
        host = socket.gethostname()  #server ip
        port = 5000  #set server port

        client_socket = socket.socket()  
        client_socket.connect((host, port))  #connect to server
        received = client_socket.recv(1024).decode()
        clock = max(clock, int(received)) + 1
        clock = clock + 1
        client_socket.send(json.dumps([clock,message]).encode())
        client_socket.close() 
    except:
        print("error occured")
    finally:
        return

if __name__ == '__main__':
    threading.Thread(target=receive_messages, args=()).start()    
    while True:
        message = input("> ")
        threading.Thread(target=client_program, args=(message,)).start()    