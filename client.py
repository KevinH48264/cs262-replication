import socket, threading, select
import grpc
import chat_pb2
import chat_pb2_grpc
import sys

# insert the server computer's IP address and port here
#server_ip_address = '10.250.73.252'
server_ip_address = "10.250.72.38"

port1 = 8080
port2 = 8081
port3 = 8082

def create_account(stub, cmd):
    return stub.CreateAccount(chat_pb2.Request(request=cmd))

def login(stub, cmd):
    return stub.LogIn(chat_pb2.Request(request=cmd))

def show_accounts(stub, cmd):
    return stub.ShowAccounts(chat_pb2.Request(request=cmd))

def send_message_to(stub, cmd):
    return stub.SendMessage(chat_pb2.Request(request=cmd))

def delete_account(stub, cmd):
    return stub.DeleteAccount(chat_pb2.Request(request=cmd))

def quit(stub, cmd):
    return stub.LogOut(chat_pb2.Request(request=cmd))

def run():
    # TODO: handle trying port 1, then port 2, then port 3. If all fail, then exit the program.

    # connect to server host and port
    with grpc.insecure_channel(('{}:{}').format(server_ip_address, port1)) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        print("YOU ARE SUCCESSFULLY CONNECTED TO THE SERVER AT PORT {}! Instructions here: 1. create_account [USERNAME] 2. show_accounts [USERNAME (optional)] 3. send_message_to [INSERT RECIPIENT] message: [INSERT MESSAGE] 5. delete_account [username] 6 (extra, logs you in): log_in [USERNAME] 7. (extra, logs you out): quit\n".format(port1))

        while True:
            try:
                message = stub.ReceiveMessage(chat_pb2.Request(request="temp"))
                if (message and message.response):
                    print(message.response)
            except Exception:
                break

            # TODO: uncomment this for Mac
            # listen to the socket or stdin for keyboard inputs.
            ready, _, _ = select.select([sys.stdin.fileno()], [], [], 0.1)

            # TODO: delete this for Mac
            #ready = [sys.stdin.fileno()]


            # once ready, check if the response is from a keyboard input (stdin) or server (socket connection)
            if ready:
                if sys.stdin.fileno() in ready:
                    # read the keyboard input
                    cmd = sys.stdin.readline()
                    res = "Waiting for a valid response... Please see instructions above."
                    # if there is a command prompt, send it and wait for a server response before printing it and continuing
                    if len(str.encode(cmd)) > 0:
                        if 'create_account' in cmd:
                            try:
                                res = create_account(stub, cmd).response
                            except Exception:
                                break
                        elif 'log_in' in cmd:
                            try:
                                res = login(stub, cmd).response
                            except Exception:
                                break                            
                        elif 'show_accounts' in cmd:
                            try:
                                res = show_accounts(stub, cmd).response
                            except Exception:
                                break       
                        elif 'send_message_to' in cmd:
                            try:
                                res = send_message_to(stub, cmd).response
                            except Exception:
                                break  

                        elif 'delete_account' in cmd:
                            try:
                                res = delete_account(stub, cmd).response
                            except Exception:
                                break  

                        elif 'quit' in cmd:
                            try:
                                res = quit(stub, cmd).response
                            except Exception:
                                break  

                    print(res)

    # connect to server host and port
    with grpc.insecure_channel(('{}:{}').format(server_ip_address, port2)) as channel:
        stub1 = chat_pb2_grpc.ChatServiceStub(channel)

        print("YOU ARE SUCCESSFULLY CONNECTED TO THE SERVER AT PORT {}! Instructions here: 1. create_account [USERNAME] 2. show_accounts [USERNAME (optional)] 3. send_message_to [INSERT RECIPIENT] message: [INSERT MESSAGE] 5. delete_account [username] 6 (extra, logs you in): log_in [USERNAME] 7. (extra, logs you out): quit\n".format(port2))

        while True:
            try:
                message = stub1.ReceiveMessage(chat_pb2.Request(request="temp"))
                if (message and message.response):
                    print(message.response)
            except Exception:
                break

            # TODO: uncomment this for Mac
            # listen to the socket or stdin for keyboard inputs.
            ready, _, _ = select.select([sys.stdin.fileno()], [], [], 0.1)

            # TODO: delete this for Mac
            #ready = [sys.stdin.fileno()]


            # once ready, check if the response is from a keyboard input (stdin) or server (socket connection)
            if ready:
                if sys.stdin.fileno() in ready:
                    # read the keyboard input
                    cmd = sys.stdin.readline()
                    res = "Waiting for a valid response... Please see instructions above."
                    # if there is a command prompt, send it and wait for a server response before printing it and continuing
                    if len(str.encode(cmd)) > 0:
                        if 'create_account' in cmd:
                            try:
                                res = create_account(stub1, cmd).response
                            except Exception:
                                break
                        elif 'log_in' in cmd:
                            try:
                                res = login(stub1, cmd).response
                            except Exception:
                                break                            
                        elif 'show_accounts' in cmd:
                            try:
                                res = show_accounts(stub1, cmd).response
                            except Exception:
                                break       
                        elif 'send_message_to' in cmd:
                            try:
                                res = send_message_to(stub1, cmd).response
                            except Exception:
                                break  

                        elif 'delete_account' in cmd:
                            try:
                                res = delete_account(stub1, cmd).response
                            except Exception:
                                break  

                        elif 'quit' in cmd:
                            try:
                                res = quit(stub1, cmd).response
                            except Exception:
                                break  
                    print(res)

    # connect to server host and port
    with grpc.insecure_channel(('{}:{}').format(server_ip_address, port3)) as channel:
        stub2 = chat_pb2_grpc.ChatServiceStub(channel)

        print("YOU ARE SUCCESSFULLY CONNECTED TO THE SERVER AT PORT {}! Instructions here: 1. create_account [USERNAME] 2. show_accounts [USERNAME (optional)] 3. send_message_to [INSERT RECIPIENT] message: [INSERT MESSAGE] 5. delete_account [username] 6 (extra, logs you in): log_in [USERNAME] 7. (extra, logs you out): quit\n".format(port3))

        while True:
            try:
                message = stub2.ReceiveMessage(chat_pb2.Request(request="temp"))
                if (message and message.response):
                    print(message.response)
            except Exception:
                break

            # TODO: uncomment this for Mac
            # listen to the socket or stdin for keyboard inputs.
            ready, _, _ = select.select([sys.stdin.fileno()], [], [], 0.1)

            # TODO: delete this for Mac
            #ready = [sys.stdin.fileno()]


            # once ready, check if the response is from a keyboard input (stdin) or server (socket connection)
            if ready:
                if sys.stdin.fileno() in ready:
                    # read the keyboard input
                    cmd = sys.stdin.readline()
                    res = "Waiting for a valid response... Please see instructions above."
                    # if there is a command prompt, send it and wait for a server response before printing it and continuing
                    if len(str.encode(cmd)) > 0:
                        if 'create_account' in cmd:
                            res = create_account(stub2, cmd).response
                        elif 'log_in' in cmd:
                            res = login(stub2, cmd).response
                        elif 'show_accounts' in cmd:
                            res = show_accounts(stub2, cmd).response
                        elif 'send_message_to' in cmd:
                            res = send_message_to(stub2, cmd).response
                        elif 'delete_account' in cmd:
                            res = delete_account(stub2, cmd).response
                        elif 'quit' in cmd:
                            res = quit(stub2, cmd).response
                    print(res)

if __name__ == '__main__':
    run()  