import socketserver
import threading

HOST = ""
PORT = 9009
lock = threading.Lock()

class UserManager:
    def __init__(self):
        self.users = {}

    def addUser(self,username,conn,addr):
        if username in sefl.users:
            conn.send('this person is already registered.\n'.encode())
            return None

        #새로운 사용자를 등록함
        lock.acquire()
        self.users[username] = (conn,addr)
        lock.release()

        self.sendMessageToAll('[%s]has entered the chat!'%username)
        print('+++people chatting[%d]' %len(self.users))

        return username

    def removeUser(self,username):
        if username not in self.users:
            return
        lock.acquire()
        del self.users[username]
        lock.release()

        self.sendMessageToAll('[%s]has left the chat.' %username)
        print('---Number of participants: [%d]' %len(self.users))

    def messageHandler(self,username,msg):
        if msg[0] != '/':
            self.sendMessageToAll('[%s]%s' %(username,msg))
            return

        if msg.strip() == '/quit':
            self.removeUser(username)
            return -1

    def sendMessageToAll(self,msg):
        for conn,addr in self.users.values():
            conn.send(msg.encode())

class MyTcpHandler(socketserver.BaseRequestHandler):
    userman = UserManager()

    def handle(self):
        print('[%s]connected' %self.client_address[0])

        try:
            username = self.registerUsername()
            msg = self.request.recv(1024)
            while msg:
                print(msg.decode())
                if self.userman.messageHandler(username,msg.decode()) == -1:
                    self.request.close()
                    break
                msg = self.request.recv(1024)

        except Exception as e:
            print(e)

        print('[%s]login cancelled' %self.client_address)
        self.userman.removeUser(username)

    def registerUsername(self):
        while True:
            self.request.send('login ID:' .encode())
            username = self.request.recv(1024)
            username = username.decode().strip()
            if self.userman.addUser(username,self.request,self.client_address):
                return username

class ChatingServer(socketserver.ThreadingMixIn,socketserver.TCPServer):
    pass

def runServer():
    print('+++The chatting server is starting.')
    print('+++To end the chat, please press Ctrl+C.')

    try:
        server = ChatingServer((HOST,PORT), MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('---The chatting server is now closed.')
        server.shutdown()
        server.server_close()

runServer()

          
    
        
    
        
