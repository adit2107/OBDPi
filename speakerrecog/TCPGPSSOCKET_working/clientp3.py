# client.py  
import socket

# create a socket object


# connection to hostname on the port.

while True:

# Receive no more than 1024 bytes

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
    try:
        host = socket.gethostname()
        port = 9991
        s.connect((host, port))
        tm = s.recv(1024)
        s.close()
        print("The time got from the server is %s" % tm.decode('ascii'))
    except:
        print("Connection reset by peer Sever closed")
