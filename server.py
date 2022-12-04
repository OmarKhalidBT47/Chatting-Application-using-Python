import platform
import threading
import socket

class Server :
    def __init__(self, ip, port, credentials:dict, qna:dict) :  # constructor
        self.ip = ip 
        self.port = port
        self.credentials = credentials
        self.running = True
        self.qna = qna # questions and answers
        self.end = 'done'

        # creating a socket server in TCP mode
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        # checking if a valid ip address is provided 
        try :
            self.s.bind((self.ip, self.port)) # binding the socket to the ip and port
        except :  
            exit('invalid ip')
        self.s.listen() # listening for connections
        print('[+] server up and running...')
        self.connections = dict() # list of connections
        self.accept_connections() # accepting connections
    def accept_connections(self) : 
        while self.running :
            # accepting connections
            conn,_ = self.s.accept() 
            # using threading module to initiate a thread for each of the clients
            # starting a thread for authenticate function
            t =threading.Thread(target=self.authenticate, args=(conn,)).start() 
    def check(self, creds) :
        username, password = creds[0], creds[1] # extracting the username and password
        print(username,password) 
        # checking if the username is present in the list of usernames
        if username in self.credentials.keys() : # if yes then check if the password is correct
            # then if the password for the user is correct or not 
            if password == self.credentials[username] : # if yes then return 'valid'
                # checking if the user already has a connection with the server
                if username not in self.connections.keys() : 
                    return 'valid'
                else :
                    return 'already logged'
            else :
                return 'invalid'
        else :
            return False
    def start_session(self, username,conn) :
        # adding the username to the connections list 
        self.connections[username] = conn # adding the connection to the list of connections
        print(self.connections) # printing the list of connections
        # creating a list of questions and sending it 
        questions = [i for i in self.qna] # creating a list of questions
        self.connections[username].send(str(','.join(questions)).encode())
        while True :
            # receiving the questions from the client
            question = conn.recv(1024).decode()
            # checking if the question is present in the list of questions
            if question in self.qna.keys() :
                # if yes then send its answers
                conn.send(self.qna[question].encode())
            # checking if the 'done' message is sent 
            elif question == self.end :
                # closing the connection and removing the username from the connections list
                self.connections[username].close()
                self.connections.pop(username)
                break
            else :
                self.connections[username].send('question is not present'.encode())
    def authenticate(self, conn) : 
        while self.running : # while the server is running
            try : 
                # receiving the credentials
                creds = conn.recv(1024).decode().split("-") # splitting the credentials
            except :
                continue
            username,password = creds[0],creds[1]
            if username and password :
                auth = self.check(creds=[username,password])
                if not auth :
                    conn.send('username not found'.encode())
                    print('not found')
                if auth :
                    if auth == 'valid' : 
                        conn.send('authenticated'.encode())
                        print('user logged in ')
                        self.start_session(username, conn)
                        return
                    elif auth == 'already logged' :
                        conn.send('logged'.encode())
                        print('already logged')
                    else :
                        conn.send('incorrect password'.encode())
                        print('incorrect password')
if __name__ == '__main__' :
    # HERE ARE THE DEFAULT CREDENTIALS 
    # you can add more
    credentials = {
        "Omar" : "hellothereomar",
        "Ziyad" : "hellothereziyad"
    }
    # these are the questions with answers
    qna = { 
        "Who was this server created by?" 
        : "Omar Khalid, Abdulla Al Rajoub, Ziyad Al Horani",
        "Exam Schedule" : 
        """
         _____________________________________
        |Week | Monday  | Wednesday | Friday  |
        |------------------------------------ | 
        |1.   | Physics | Chemistry | Computer|
        |2.   | Maths   | Computer  | Physics |
        |3.   | Maths   | Chemistry | Physics |
        |4.   | Computer| Maths    | Computer |
        |_____________________________________|
        """,
        "Sport Activities" : 
        """
         ______________________________________________
        |  SPORTS FEST ON DECEMBER 21-23 2022          |
        |----------------------------------------------| 
        |21.   | Football  | Cricket       | Basketball|
        |22.   | Tennis    | Rugby         | Swimming  |
        |23.   | Cycling   | Running race  |  Shooting |
        |______________________________________________|
        """, 
        "cpu information" : str(platform.processor())
    }
    # calling the Server class and initiating 
    server = Server(ip='', port=8081,credentials=credentials, qna = qna) # ip is empty because we are using localhost