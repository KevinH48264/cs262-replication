import socket, select
import sys

# insert the server computer's IP address and port here
host = '10.250.253.162'
port = 9895

# create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to server host and port
s.connect((host, port))

# Waiting for response from server that there was a successful connection
print(str(s.recv(1024),"utf-8"), end="")

# stop connection by using Ctrl+C, otherwise continually listen to the server once connected
while True:
    # listen to the socket or stdin for keyboard inputs.
    ready, _, _ = select.select([s.fileno(), sys.stdin.fileno()], [], [], 0.1)
    
    # once ready, check if the response is from a keyboard input (stdin) or server (socket connection)
    if ready:
        if s.fileno() in ready:
            # decode and print the encoded socket message
            response = str(s.recv(1024),"utf-8")
            print(response, end="")

        elif sys.stdin.fileno() in ready:
            # read the keyboard input
            cmd = sys.stdin.readline()
            
            # if there is a command prompt, send it to the socket and wait for a server response before printing it and continuing
            if cmd:
                s.send(str.encode(cmd))
                response = str(s.recv(1024),"utf-8")
                print(response, end="")

