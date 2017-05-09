
import serverclass
import clientclass
import multiprocessing
import time
import sys
import os

#COMMANDS
GETUSERS = "RUN GETUSERS" #Connects user to peers in network
ENDCONN  = "RUN ENDCONNECTION" #Ends connection with user to peers


def clientAction(q,fileno):
    sys.stdin = os.fdopen(fileno)  #open stdin in this process
    client    = clientclass.Client()

    client.getPortsUsed()
    #print(client.ports)
    if(input()==GETUSERS): #command to get all users
        #get all current ports from database
        if(client.connectClient()):
            message ="CLIENT HAS CONNECTED"
            while message!='ENDCONN':
                client.sendMessage(message)
                message = input('->')
        else:
            print("connection failed")


def serverAction():
    server = serverclass.Server('localhost',8000)
    server.connectServer()
    port   = server.port
    print("port in use = ", port)
    #upload port used to client
    print("socket connected")
    server.connectClient()
    server.acceptClients()

q = multiprocessing.Queue()
fn = sys.stdin.fileno() #get original file descriptor for stdin
client = multiprocessing.Process(target=clientAction,args=(q,fn))
server = multiprocessing.Process(target=serverAction)
server.start()
time.sleep(2)
client.start()
client.join()
server.join()