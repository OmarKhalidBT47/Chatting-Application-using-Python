import time
import socket

class Client :
    def __init__(self, ip, port) : 
        self.ip = ip 
        self.port = port
        self.authenticated = False
        self.running = True
        self.end = 'done'

        # initiating a client socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
        self.s.connect((self.ip,self.port)) # Connecting to the server
        print('[+] Connected to server')

        while not self.authenticated  : # while user is not authenticated
            # getting the username and password from the user
            username = str(input('Enter the username : ')).strip() # removing the spaces
            password = str(input('Enter the password : ')).strip() # removing the spaces
            self.login(username,password) # calling the login function
        self.session() # calling the session function
    def login(self, username,password) : #
        # converting username and password to username-password
        creds = '-'.join([username, password]) # joining the username and password with a dash
        # sending the username and password
        self.s.send(creds.encode()) # sending the username and password to the server
        resp = self.s.recv(1024).decode() # getting the response from the server

        if resp == 'authenticated' : 
            print('[+] Logged in')
            self.authenticated = True # setting the authenticated to true
        elif resp == 'username not found' : 
            print('[!] Username no found')
        elif  resp == 'logged' :
            print('[!] User is already logged in to the server ')
        elif resp == 'incorrect password' :
            print('[!] Incorrect password')
        else :
            # server may send raw bytes b''
            pass
    def session(self) :  
        # getting the list of questions from the server
        questions = self.s.recv(4098).decode() # getting the list of questions from the server
        if questions : # if the questions are not empty
            print('Questions from server :\n', questions)
        while self.running :  # while the client is running
            # aking the user for the question
            question = str(input('Enter the question :')) # getting the question from the user
            if question == ''  : # if the question is empty
                continue 
            self.s.send(question.encode()) # sending the question to the server
            if question == self.end :  # if the question is done
                self.s.close() # closing the socket
                self.running = False # setting the running to false
                exit('Thanks for using out service') # exiting the program
            answer = self.s.recv(1024).decode() # getting the answer from the server

            if answer : 
                if answer == 'question is not present' : 
                    print('Question is invalid')
                else : 
                    print(answer)   
            time.sleep(0.1)

if __name__ == '__main__' : 
    # Enter the client ip here 
    clinet = Client(ip='10.0.17.125', port=8081)  # creating a client object