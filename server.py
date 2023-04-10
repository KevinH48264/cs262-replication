import re
import grpc
import re
from concurrent import futures
import chat_pb2
import chat_pb2_grpc
import sys
import csv
import os
import threading
import time

# insert the server computer's IP address and port here. Ports reflect the 3 servers that are running for the backend. Lowest number will be the primary in case of leader election.
#ip = "10.250.73.252"
ip = "10.250.72.38"
ports = [8080, 8081, 8082]
ports_alive = [True, True, True]

class ChatServicer(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self, port):
        print("Starting ChatServicer on port ", port)

        # this is the object that stores { username : connection (if logged in) } as a key : value dictionary that runs when the server starts, keeping track of all usernames and their connections if they are connected
        self.accounts = {}
        # this is the object that stores { username : [] (list of messages) } as a key : value dictionary that runs when the server starts, this tracks any messages in queue to be delivered to the user from other users
        self.queues = {}

        self.port = port
        self.primary = False
        self.other_servers = []
        for i in ports:
            if i != int(port):
                self.other_servers.append(i)

        # Check heartbeats of other servers to see if they are alive. If not, then set self.primary to True
        heartbeat_thread = threading.Thread(target=self.send_heartbeat)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()

        # Check if accounts.csv exists, if not, create it
        if not os.path.exists(f'accounts-{port}.csv'):
            with open(f'accounts-{port}.csv', mode='w'):
                pass

        # Load accounts data from accounts.csv
        with open(f'accounts-{port}.csv', mode='r') as infile:
            reader = csv.reader(infile)
            for rows in reader:
                if len(rows) == 2:
                    self.accounts[rows[0]] = rows[1]

        # Check if queues.csv exists, if not, create it
        if not os.path.exists(f'queues-{port}.csv'):
            with open(f'queues-{port}.csv', mode='w'):
                pass

        # Load message queues data from queues.csv, format of messages will be separated by |
        with open(f'queues-{port}.csv', mode='r') as infile:
            reader = csv.reader(infile)
            for rows in reader:
                if len(rows) == 2:
                    self.queues[rows[0]] = rows[1].split('|')

        print("Accounts: ", self.accounts)
        print("Queues: ", self.queues)

    # create the username and store their connection if the username is unique
    def CreateAccount(self, request, context):
        global ports_alive
        global ports

        print("create account!")

        username = request.request[15:].strip("\n")
        if username in list(self.accounts.keys()):
            return chat_pb2.Response(response="This username already exists. If this is your account, please log in. If not, create an account with a different username.") 
        else:
            self.accounts[username] = context.peer()
            self.queues[username] = []

            # commiting log
            print("committing!")
            save_accounts(self.accounts, self.port)
            save_queues(self.queues, self.port)

            # send to replicas before responding to client
            if self.primary:
                print("send to replicas!")
                for replica in self.other_servers:
                    print("ports_alive[ports.index(replica)]", ports_alive[ports.index(replica)])
                    if ports_alive[ports.index(replica)]:
                        channel = grpc.insecure_channel(ip + ":" + str(replica))
                        stub = chat_pb2_grpc.ReplicationServiceStub(channel)
                        account_update = chat_pb2.AccountUpdate(username=username, connection=context.peer())
                        stub.UpdateAccount(account_update)
                        queue_update = chat_pb2.QueueUpdate(username=username, messages=[])
                        stub.UpdateQueue(queue_update)

            print("User {} created!".format(username))
            return chat_pb2.Response(response="Account {} created!".format(username)) 

    # log username in and update active connection if the username exists
    def LogIn(self, request, context):
        username = request.request[7:].strip("\n")
        if username in list(self.accounts.keys()):
            self.accounts[username] = context.peer()

            # commiting log
            print("committing!")
            save_accounts(self.accounts, self.port)
            save_queues(self.queues, self.port)

            # send to replicas before responding to client
            if self.primary:
                print("send to replicas!")
                for replica in self.other_servers:
                    print("ports_alive[ports.index(replica)]", ports_alive[ports.index(replica)])
                    if ports_alive[ports.index(replica)]:
                        channel = grpc.insecure_channel(ip + ":" + str(replica))
                        stub = chat_pb2_grpc.ReplicationServiceStub(channel)
                        account_update = chat_pb2.AccountUpdate(username=username, connection=context.peer())
                        stub.UpdateAccount(account_update)
                        queue_update = chat_pb2.QueueUpdate(username=username, messages=self.queues[username])
                        stub.UpdateQueue(queue_update)

            print("User {} logged in!".format(username))
            return chat_pb2.Response(response="{} is successfully logged in!".format(username))
        else:
            return chat_pb2.Response(response="This account does not exist, but the username is available. Please create an account first.")

    # send a message from recipient to sender based on the input command from client
    def SendMessage(self, request, context):
        recipient = request.request[16:request.request.find("message: ") - 1]
        message = request.request[request.request.find("message: ") + 9:]

        # recipient account does not exist
        if recipient not in list(self.accounts.keys()):
            return chat_pb2.Response(response="error: the recipient " + recipient + " does not exist, please have them create an account before you can send a message to them")

        elif self.accounts[recipient] is None:
            # recipient is offline and message should be stored in queue
            sender = list(self.accounts.keys())[list(self.accounts.values()).index(context.peer())]
            self.queues[recipient].append(sender + " sent you a message: " + message)

            # commiting log
            print("committing!")
            save_queues(self.queues, self.port)

            # send to replicas before responding to client
            if self.primary:
                print("send to replicas!")
                for replica in self.other_servers:
                    print("ports_alive[ports.index(replica)]", ports_alive[ports.index(replica)])
                    if ports_alive[ports.index(replica)]:
                        channel = grpc.insecure_channel(ip + ":" + str(replica))
                        stub = chat_pb2_grpc.ReplicationServiceStub(channel)
                        queue_update = chat_pb2.QueueUpdate(username=recipient, messages=self.queues[recipient])
                        stub.UpdateQueue(queue_update)

            return chat_pb2.Response(response="message will be sent to {} when they log in".format(recipient))

        # recipient is online and message will be sent immediately
        else:
            sender = list(self.accounts.keys())[list(self.accounts.values()).index(context.peer())]
            self.queues[recipient].append(sender + " sent you a message: " + message)          

            # commiting log
            print("committing!")
            save_queues(self.queues, self.port)

            # send to replicas before responding to client
            if self.primary:
                print("send to replicas!")
                for replica in self.other_servers:
                    print("ports_alive[ports.index(replica)]", ports_alive[ports.index(replica)])
                    if ports_alive[ports.index(replica)]:
                        channel = grpc.insecure_channel(ip + ":" + str(replica))
                        stub = chat_pb2_grpc.ReplicationServiceStub(channel)
                        queue_update = chat_pb2.QueueUpdate(username=recipient, messages=self.queues[username])
                        stub.UpdateQueue(queue_update)

            return chat_pb2.Response(response="message successfully sent to {}".format(recipient))

    # return all accounts that fulfill regex matching
    def ShowAccounts(self, request, context):
        print("showing accounts!")

        # Parsing command line input from client
        search_input = request.request[14:].strip("\n")

        # regex matching
        regex = re.compile(search_input)
        matches = []
        matches = [string for string in list(self.accounts.keys()) if re.match(regex, string) is not None]

        # return a string that contains all the regex matched accounts
        final_accounts = ""
        for i in range(len(matches)):
            final_accounts += matches[i] + "\n"

        print("final accounts: ", final_accounts)

        return chat_pb2.Response(response=final_accounts)

    # delete all information related to the username from accounts and queues dictionary
    def DeleteAccount(self, request, context):
        try:
            account_to_be_deleted = list(self.accounts.keys())[list(self.accounts.values()).index(context.peer())]
        
        except ValueError:
            return chat_pb2.Response(response="You are currently not logged in. Please log in first in order to delete your account.")

        self.accounts.pop(account_to_be_deleted)
        self.queues.pop(account_to_be_deleted)

        # commiting log
        print("committing!")
        save_accounts(self.accounts, self.port)
        save_queues(self.queues, self.port)

        # send to replicas before responding to client
        if self.primary:
            print("send to replicas!")
            for replica in self.other_servers:
                print("ports_alive[ports.index(replica)]", ports_alive[ports.index(replica)])
                if ports_alive[ports.index(replica)]:
                    channel = grpc.insecure_channel(ip + ":" + str(replica))
                    stub = chat_pb2_grpc.ReplicationServiceStub(channel)
                    account_update = chat_pb2.AccountUpdate(username=username, connection=None)
                    stub.DeleteAccount(account_update)
                    queue_update = chat_pb2.QueueUpdate(username=username, messages=[])
                    stub.DeleteQueue(queue_update)

        return chat_pb2.Response(response="The account {} has been successfully deleted.".format(account_to_be_deleted))

    # The client [USERNAME] uses this function to constantly query the server for whether it has received any messages, by sending and emptying queues[USERNAME]
    def ReceiveMessage(self, request, context):
        try:
            receiving_user = list(self.accounts.keys())[list(self.accounts.values()).index(context.peer())]
        except:
            return chat_pb2.Response(response="")
        messages = self.queues[receiving_user]
        final_messages = ""
        if len(messages) > 0:
            for i in range(len(messages)):
                final_messages += messages[i] + "\n"

            # Empty the queue after all messages have been sent
            self.queues[receiving_user] = []

            # commiting log
            print("committing!")
            save_accounts(self.accounts, self.port)
            save_queues(self.queues, self.port)

            # send to replicas before responding to client
            if self.primary:
                print("send to replicas!")
                for replica in self.other_servers:
                    print("ports_alive[ports.index(replica)]", ports_alive[ports.index(replica)])
                    if ports_alive[ports.index(replica)]:
                        channel = grpc.insecure_channel(ip + ":" + str(replica))
                        stub = chat_pb2_grpc.ReplicationServiceStub(channel)
                        account_update = chat_pb2.AccountUpdate(username=receiving_user, connection=context.peer())
                        stub.UpdateAccount(account_update)
                        queue_update = chat_pb2.QueueUpdate(username=receiving_user, messages=self.queues[receiving_user])
                        stub.UpdateQueue(queue_update)

            return chat_pb2.Response(response=final_messages)

        else:
           return chat_pb2.Response(response="")

    # Allow clients to quit connection and log out
    def LogOut(self, request, context):
        print(context.peer())
        print("account keys: ", list(self.accounts.keys()))
        print("account values: ", list(self.accounts.values()))
        username = list(self.accounts.keys())[list(self.accounts.values()).index(context.peer())]
        self.accounts[username] = None

        # commiting log
        print("committing!")
        save_accounts(self.accounts, self.port)
        save_queues(self.queues, self.port)

        # send to replicas before responding to client
        if self.primary:
            print("send to replicas!")
            for replica in self.other_servers:
                print("ports_alive[ports.index(replica)]", ports_alive[ports.index(replica)])
                if ports_alive[ports.index(replica)]:
                    channel = grpc.insecure_channel(ip + ":" + str(replica))
                    stub = chat_pb2_grpc.ReplicationServiceStub(channel)
                    account_update = chat_pb2.AccountUpdate(username=receiving_user, connection=None)
                    stub.UpdateAccount(account_update)
                    queue_update = chat_pb2.QueueUpdate(username=receiving_user, messages=self.queues[receiving_user])
                    stub.UpdateQueue(queue_update)

        return chat_pb2.Response(response="successfully quit / logged off")
    
    # A function that allows for other servers to check if this server is still alive
    def SendHeartbeat(self, request, context):
        return chat_pb2.Response(response="server is alive")
    
    # Checks on other servers
    def send_heartbeat(self, interval=1):
        global ip

        while True:
            print("- send_heartbeat status, ports_alive", ports_alive)
            time.sleep(interval)
            for backup_server in self.other_servers:
                channel = grpc.insecure_channel(ip + ":" + str(backup_server))
                stub = chat_pb2_grpc.ChatServiceStub(channel)

                try:
                    # if the heartbeat is successful, the server is alive
                    response = stub.SendHeartbeat(chat_pb2.Request(request="temp"))
                    print(f"- Heartbeat received from {backup_server}: {response.response}")
                    ports_alive[ports.index(backup_server)] = True

                except grpc.RpcError as e:
                    # else the heartbeat was not successful, the server is dead, run leader election
                    print(f"- Failed to send heartbeat to {backup_server}")

                    # only run leader election if the server is not already dead
                    if ports_alive[ports.index(backup_server)]:
                        ports_alive[ports.index(backup_server)] = False
                        self.leader_election()
    
    # Leader election
    def leader_election(self):
        print("- running leader election")

        # the lowest alive port number is the primary server
        if ports.index(int(self.port)) == ports_alive.index(True):
            print("- I am the primary server")
            self.primary = True
        else:
            print("- I am not the primary server")

        return


# ReplicationServicer class for receiving updates from primary as replica
class ReplicationServicer(chat_pb2_grpc.ReplicationServiceServicer):
    def __init__(self, chat_servicer, port):
        self.chat_servicer = chat_servicer
        self.port = port

    def UpdateAccount(self, request, context):
        self.chat_servicer.accounts[request.username] = request.connection
        save_accounts(self.chat_servicer.accounts, self.port)
        return chat_pb2.Response(response="Account updated")

    def UpdateQueue(self, request, context):
        self.chat_servicer.queues[request.username] = request.messages
        save_queues(self.chat_servicer.queues, self.port)
        return chat_pb2.Response(response="Queue updated")

    def DeleteAccount(self, request, context):
        self.chat_servicer.accounts.pop(request.username)
        save_accounts(self.chat_servicer.accounts, self.port)
        return chat_pb2.Response(response="Account updated")

    def DeleteQueue(self, request, context):
        self.chat_servicer.queues.pop(request.username) 
        save_queues(self.chat_servicer.queues, self.port)
        return chat_pb2.Response(response="Queue updated")

# helper functions for both ChatServicer and ReplicationServicer
def save_accounts(accounts, port):
    with open(f'accounts-{port}.csv', mode='w') as outfile:
        writer = csv.writer(outfile)
        for key, value in accounts.items():
            writer.writerow([key, value])

def save_queues( queues, port):
    with open(f'queues-{port}.csv', mode='w') as outfile:
        writer = csv.writer(outfile)
        for key, value in queues.items():
            writer.writerow([key, '|'.join(value)])


# main function
def run_server(port=8080):
    print("starting server")
    global ip

    # create a server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_servicer = ChatServicer(port)
    chat_pb2_grpc.add_ChatServiceServicer_to_server(chat_servicer, server)
    chat_pb2_grpc.add_ReplicationServiceServicer_to_server(ReplicationServicer(chat_servicer, port), server)
    server.add_insecure_port(ip + ":" + port)
    server.start()
    
    print('Server is running...')
    server.wait_for_termination()

# run "python server.py 8080"
if __name__ == '__main__':
    run_server(sys.argv[1])