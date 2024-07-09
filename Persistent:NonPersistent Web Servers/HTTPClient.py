from socket import *
import sys
import re
from signal import signal, SIGPIPE, SIG_DFL   
signal(SIGPIPE,SIG_DFL) 
from time import time

def parse_filenames(html_content):
    # Use regular expression to find file names ending in .jpg or .txt
    filenames = re.findall(r'data="(.+\.(jpg|txt))"', html_content)
    return [filename[0] for filename in filenames]

def np_http(serverH, serverP, file): #non-persistent http
    httpClient = socket(AF_INET, SOCK_STREAM)
    httpClient.connect((serverH, serverP))
    start = time()
    request = "GET /%s HTTP/1.1\r\n Connection: close\r\n\r\n" %(file)
    httpClient.sendall(request.encode())

    response = b""
    while True:
        data = httpClient.recv(4096)
        if not data:
            break
        response += data
    htmlFileContent = response.decode()
    #print(htmlFileContent)
    httpClient.close()

    filenames = parse_filenames(htmlFileContent)
    #print(filenames)

    for filename in filenames:
        httpClient = socket(AF_INET, SOCK_STREAM)
        httpClient.connect((serverH, serverP))

        request = "GET /%s HTTP/1.1\r\n Connection: close\r\n\r\n" %(filename)
        httpClient.sendall(request.encode())
        response = b""
        while True:
            data = httpClient.recv(4096)
            if not data:
                break
            response += data
        #print(response.decode())
        print(str(filename) + " done")
        
        httpClient.close()
    end = time()
    elapsed = (end - start)
    print("Total Time: " + str(elapsed) + "s")

def p_http(serverH, serverP, file): #persistent http
    httpClient = socket(AF_INET, SOCK_STREAM)
    httpClient.connect((serverH, serverP))
    httpClient.settimeout(0.001)
    start = time()
    request = "GET /%s HTTP/1.1\r\n Connection: keep-alive\r\n Accept: image/*, text/*\r\n\r\n" %(file)
    httpClient.sendall(request.encode())
    #print("request sent")


    htmlFileContent = ""
    while True:
        try:
            data = httpClient.recv(10000)
        except TimeoutError:
            break
        htmlFileContent += data.decode()
        #print(htmlFileContent)
            
    filenames = parse_filenames(htmlFileContent)
    #print(filenames)


    for filename in filenames:
        request = "GET /%s HTTP/1.1\r\n Connection: keep-alive\r\n Accept: image/*, text/*\r\n\r\n" %(filename)
        httpClient.sendall(request.encode())
        #print("request sent")

        response = b""
        while True:
            try:
                data = httpClient.recv(10000)
            except TimeoutError:
                break
            response += data
        #print(response.decode())
        if(response):
            print(str(filename) + " done")
   
    
    end = time()
    elapsed = (end - start)
    print("Total Time: " + str(elapsed) + "s")
    httpClient.close()



if __name__ == "__main__":
    serverHost = sys.argv[1]
    serverPort = int(sys.argv[2])
    filePath = sys.argv[3]

    #comment one out to test each HTTP implementation separately
    
    #np_http(serverHost, serverPort, filePath)
    p_http(serverHost, serverPort, filePath)







