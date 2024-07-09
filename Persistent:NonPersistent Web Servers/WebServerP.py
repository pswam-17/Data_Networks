#PERSISTENT HTTP

from socket import *
import sys # In order to terminate the program
from signal import signal, SIGPIPE, SIG_DFL   
signal(SIGPIPE,SIG_DFL) 
import time



serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a sever socket
#Fill in start
serverPort = 6810
serverSocket.bind(('127.0.0.1', serverPort))
serverSocket.listen(1)
#Fill in end



while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        while True:
            message = connectionSocket.recv(1024)
            if not message:
                print("no message received")
                break
            filename = message.split()[1]
            print(filename)
            namecheck = str(filename[1:].decode())
            #code outputdata to read both text files and image files 
            with open(filename[1:], 'rb') as f:
                output = f.read()
            if(namecheck.endswith(".jpg")):
                outputdata = str(output)
            else:
                outputdata = output.decode()
            #Send one HTTP header line into socket
            #Fill in start
            connectionSocket.send('\nHTTP/1.1 200 OK\n\n'.encode())
        
            #Fill in end
            #Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
            # encode the string using the provided encoding. This function returns the bytes object. If we don’t provide encoding, “utf-8” encoding is used as default.
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())
        
        connectionSocket.close()


    except IOError:
        # Send HTTP response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        # Close the client connection socket
        connectionSocket.close()
        serverSocket.close()


serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data
