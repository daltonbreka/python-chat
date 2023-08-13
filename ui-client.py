import sys
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import socket
import json
import threading
from datetime import *
import os
from threading import Event

clientPort = 5002
serverPort = 5000

class filedialogdemo(QWidget):
    def __init__(self, parent = None):
        super(filedialogdemo, self).__init__(parent)

        self.setGeometry(200,200,600,600)
        self.setFont(QFont("Arial",20))

        layout = QVBoxLayout()
        
        self.contents = QTextEdit()
        self.contents.setReadOnly(True)
        layout.addWidget(self.contents)
        
        layout2 = QHBoxLayout()
        
        self.serverIp = QLineEdit()
        self.serverIp.setFixedWidth(200)
        self.serverIp.setText("127.0.0.1")
        layout2.addWidget(self.serverIp)
        
        self.message = QLineEdit()
        self.message.setText("Here is message")
        self.message.returnPressed.connect(self.sendMessage)
        layout2.addWidget(self.message)
        layout.addLayout(layout2)
        
        self.setLayout(layout)
        self.setWindowTitle("Chat Demo")
        self.setWindowIcon(QIcon("icon.png"))

        self.clock = 1

        self.even = Event()
        self.thread = threading.Thread(target=self.receive_messages, args=(self.even,))
        self.thread.start()

    def sendMessage(self,):
        data = self.message.text()
        if len(data) and self.isValidServerIp() :
            threading.Thread(target=self.client_program, args=(data,)).start() 
            self.message.setText("")
    
    def isValidServerIp(self,):
        ip = self.serverIp.text()
        return True

    def receive_messages(self,event):
        global clientPort
        host = socket.gethostname()
        server_socket = socket.socket()  
        server_socket.bind((host, clientPort))  
        server_socket.listen(1)
        while True:
            # if event.is_set():
            #     break
            client, _ = server_socket.accept()
            received = client.recv(1024)
            if len(received) > 0 :
                messages = json.loads(received)
                for message in messages:
                    self.append_message("message: " + message[0])
                    self.append_message("timestamp: " + str(message[1]))
            client.close()

    def append_message(self, message):
        self.contents.moveCursor(QTextCursor.End)
        self.contents.insertPlainText(f' {message}\n')
        # scroll to bottom
        
    def client_program(self,message):
        global serverPort
        try:

            client_socket = socket.socket()  
            print(self.serverIp.text())
            client_socket.connect((self.serverIp.text(), serverPort))  #connect to server
            received = client_socket.recv(1024).decode()
            self.clock = max(self.clock, int(received)) + 1
            self.clock = self.clock + 1
            client_socket.send(json.dumps([self.clock,message]).encode())
            client_socket.close() 
        except:
            print("error occured")
        finally:
            return
        
    def closeEvent(self, a0: QCloseEvent) -> None:
        super().closeEvent(a0)
        return

def main():
    app = QApplication(sys.argv)
    ex = filedialogdemo()
    ex.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()