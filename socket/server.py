import socket
import _thread
import re

# insert the server computer's IP address and port here
host = "10.250.253.162"
port = 9895

# this is the object that stores { username : connection (if logged in) } as a key : value dictionary that runs when the server starts, keeping track of all usernames and their connections if they are connected
accounts = {}

# this is the object that stores { username : [] (list of messages) } as a key : value dictionary that runs when the server starts, this tracks any messages in queue to be delivered to the user from others
queues = {}

# Create a Socket (connect client and server computers)
def create_socket():
    try:
        global host
        global port
        global s
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Establish connection with a client (socket must be listening)
def socket_accept():
    while True:
        conn, address = s.accept()
        print("Connection has been established! |" + " IP " + address[0] + " | Port" + str(address[1]))

        # allow for multiple connections to be made using threads
        _thread.start_new_thread(receive_commands, (conn,))

# Send commands to client
def receive_commands(conn):
    conn.send(str.encode("YOU ARE SUCCESSFULLY CONNECTED TO THE SERVER! Instructions here: 1. create_account [USERNAME] 2. show_accounts [USERNAME (optional)] 3. send_message_to [INSERT RECIPIENT] message: [INSERT MESSAGE] 5. delete_account [username] 6 (extra, logs you in): log_in [USERNAME] 7. (extra, logs you out): quit\n"))

    # always listen for data from the client through the socket connection
    while True:
        # debug statement to help maintain states of the protocol buffers
        # print("current info: ", accounts, queues)

        # always listen for data and store the response in the res variable, saying waiting for valid response if none of the commands are recognized
        data = conn.recv(1024)

        # if no data, the connection was likely closed -- break
        if not data:
            break

        input_cmd = data.decode("utf-8")
        res = "Waiting for valid response..."

        # Allow client to 1. create an account and supply a unique user name
        # Input format should be: create_account [USERNAME]
        if 'create_account' in input_cmd:
            # create_account + space is 15 characters
            username = input_cmd[15:].strip("\n")
            res = create_account(username, conn)

        # Allow clients to log in
        elif 'log_in' in input_cmd:
            # log_in + space is 7 characters
            username = input_cmd[7:].strip("\n")
            res = log_in(username, conn)

            # Server delivers undelivered messages to a particular user if they logged in
            res += check_queue(username, conn)

        # Allow client to list accounts by text wildcard
        elif 'show_accounts' in input_cmd:
            # show_accounts + space is 14 characters
            username = input_cmd[14:].strip("\n")
            res = show_accounts(username)

        # Allow client to send a message to a recipient, and queue if the recipient isn't logged in
        # to send a message: "send_message_to [INSERT RECIPIENT] message: [INSERT MESSAGE]"
        # print(input_cmd)
        elif 'send_message_to' in input_cmd:
            res = send_message(input_cmd, conn)

        # Allow client to delete an account
        elif 'delete_account' in input_cmd:
            res = delete_account(conn)

        # Allow clients to quit connection
        elif 'quit' in input_cmd[:4]:
            # mark that the sender has closed their connection
            sender = list(accounts.keys())[list(accounts.values()).index(conn)]
            accounts[sender] = None
            res = "successfully quit / logged off"

        # send the response back to the client
        conn.send(str.encode(res + "\n"))

# send messages in queue to user when they log in, if they have messages. Once sent, remove message from queue
def check_queue(user, conn):
    messages = ""
    for msg in queues[user]:
        #conn.send(str.encode(msg))
        messages += "\n" + msg
        queues[user].remove(msg)
    return messages

# send a message from recipient to sender based on the input command from client
def send_message(input_cmd, conn):
    # ensure the formatting for sending a message is correct
    if 'message: ' not in input_cmd:
        res = "please send a message using this format: 'send_message_to [INSERT RECIPIENT] message: [INSERT MESSAGE]'"
    
    # parse the command to figure out how the recipient is and what the message is
    recipient = input_cmd[16:input_cmd.find("message: ") - 1]
    message = input_cmd[input_cmd.find("message: ") + 9:]

    # ensure that the recipient account exists
    if recipient in list(accounts.keys()): 
        # recipient exists
        recipient_conn = accounts[recipient]
        sender = list(accounts.keys())[list(accounts.values()).index(conn)]

        # recipient has an active connection and message is delivered, sender is notified of successful send
        if recipient_conn:
            recipient_conn.send(str.encode(sender + " sent you a message: " + message))
            res = "message successfully sent to {}".format(recipient)

        # recipient is offline and message should be stored in queue, sender is notified of status
        else:
            queues[recipient].append(sender + " sent you a message: " + message)
            res = "message will be sent to {} when they log in".format(recipient)
    
    # recipient does not exist, return error message
    else:
        res = "error: the recipient " + recipient + " does not exist, please have them create an account before you can send a message to them"
    
    return res

# log username in and update active connection if the username exists
def log_in(username, conn):
    if username in list(accounts.keys()):
        accounts[username] = conn
        return "{} is successfully logged in!".format(username)
    else:
        return "This account does not exist, but the username is available. Please create an account first."

# create the username and store their connection if the username is unique
def create_account(username, conn):
    if username in list(accounts.keys()):
        return "This username already exists. If this is your account, please log in. If not, create an account with a different username."
    else:
        accounts[username] = conn
        queues[username] = []
        return "account_created"

# delete all information related to the username from accounts and queues dictionary
def delete_account(conn):
    # find the current account username based on the active connection
    try:
        account_to_be_deleted = list(accounts.keys())[list(accounts.values()).index(conn)]
    except ValueError:
        return "You are currently not logged in. Please log in first in order to delete your account."

    accounts.pop(account_to_be_deleted)
    queues.pop(account_to_be_deleted)
    return "The account {} has been successfully deleted.".format(account_to_be_deleted)

# return all accounts that fulfill regex matching
def show_accounts(search_input):
    regex = re.compile(search_input)
    matches = []
    matches = [string for string in list(accounts.keys()) if re.match(regex, string) is not None]
    print("matches:", matches)
    final_accounts = ""
    for i in range(len(matches)):
        final_accounts += matches[i] + " "
    return final_accounts

# create the socket, bind to the socket, and accept connections as a server
def run_server():
    create_socket()
    bind_socket()
    socket_accept()

if __name__ == '__main__':
    run_server()