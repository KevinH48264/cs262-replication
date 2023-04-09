'''
To run, go to this directory and run 'pytest -v'
'''

import grpc
import time
import chat_pb2_grpc
import _thread
from server import run_server, ip, port
from client import create_account, login, show_accounts, send_message_to, delete_account, quit

# run the server in background
_thread.start_new_thread(run_server, ())

time.sleep(0.5)

# test create account
def test_create_account():
    global ip
    global port

    # create a client socket
    with grpc.insecure_channel(('{}:{}').format(ip, port)) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        # send the create_account message
        cmd = "create_account bob"
        res = "Waiting for a valid response... Please see instructions above."
        # if there is a command prompt, send it and wait for a server response before printing it and continuing
        if len(str.encode(cmd)) > 0:
            if 'create_account' in cmd:
                res = create_account(stub, cmd).response
            if 'log_in' in cmd:
                res = login(stub, cmd).response
            if 'show_accounts' in cmd:
                res = show_accounts(stub, cmd).response
            if 'send_message_to' in cmd:
                res = send_message_to(stub, cmd).response
            if 'delete_account' in cmd:
                res = delete_account(stub, cmd).response
            if 'quit' in cmd:
                res = quit(stub, cmd).response

        # store the response
        assert(res == "Account bob created!")

def test_create_account_non_unique():
    global ip
    global port

    # create a client socket
    with grpc.insecure_channel(('{}:{}').format(ip, port)) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        # send the create_account message
        cmd = "create_account bob"
        res = "Waiting for a valid response... Please see instructions above."
        # if there is a command prompt, send it and wait for a server response before printing it and continuing
        if len(str.encode(cmd)) > 0:
            if 'create_account' in cmd:
                res = create_account(stub, cmd).response
            if 'log_in' in cmd:
                res = login(stub, cmd).response
            if 'show_accounts' in cmd:
                res = show_accounts(stub, cmd).response
            if 'send_message_to' in cmd:
                res = send_message_to(stub, cmd).response
            if 'delete_account' in cmd:
                res = delete_account(stub, cmd).response
            if 'quit' in cmd:
                res = quit(stub, cmd).response

        # send the create_account message
        cmd = "create_account bob"
        res = "Waiting for a valid response... Please see instructions above."
        # if there is a command prompt, send it and wait for a server response before printing it and continuing
        if len(str.encode(cmd)) > 0:
            if 'create_account' in cmd:
                res = create_account(stub, cmd).response
            if 'log_in' in cmd:
                res = login(stub, cmd).response
            if 'show_accounts' in cmd:
                res = show_accounts(stub, cmd).response
            if 'send_message_to' in cmd:
                res = send_message_to(stub, cmd).response
            if 'delete_account' in cmd:
                res = delete_account(stub, cmd).response
            if 'quit' in cmd:
                res = quit(stub, cmd).response

        # store the response
        assert(res == "This username already exists. If this is your account, please log in. If not, create an account with a different username.")

def test_create_second_unique_account():
    global ip
    global port

    # create a client socket
    with grpc.insecure_channel(('{}:{}').format(ip, port)) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        # send the create_account message
        cmd = "create_account andy"
        res = "Waiting for a valid response... Please see instructions above."
        # if there is a command prompt, send it and wait for a server response before printing it and continuing
        if len(str.encode(cmd)) > 0:
            if 'create_account' in cmd:
                res = create_account(stub, cmd).response
            if 'log_in' in cmd:
                res = login(stub, cmd).response
            if 'show_accounts' in cmd:
                res = show_accounts(stub, cmd).response
            if 'send_message_to' in cmd:
                res = send_message_to(stub, cmd).response
            if 'delete_account' in cmd:
                res = delete_account(stub, cmd).response
            if 'quit' in cmd:
                res = quit(stub, cmd).response

        # store the response
        assert(res == "Account andy created!")


def test_show_accounts():
    global ip
    global port

    # create a client socket
    with grpc.insecure_channel(('{}:{}').format(ip, port)) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        # send the create_account message
        cmd = "show_accounts"
        res = "Waiting for a valid response... Please see instructions above."
        # if there is a command prompt, send it and wait for a server response before printing it and continuing
        if len(str.encode(cmd)) > 0:
            if 'create_account' in cmd:
                res = create_account(stub, cmd).response
            if 'log_in' in cmd:
                res = login(stub, cmd).response
            if 'show_accounts' in cmd:
                res = show_accounts(stub, cmd).response
            if 'send_message_to' in cmd:
                res = send_message_to(stub, cmd).response
            if 'delete_account' in cmd:
                res = delete_account(stub, cmd).response
            if 'quit' in cmd:
                res = quit(stub, cmd).response

        # store the response
        assert(res == "bob\nandy\n")


def test_show_accounts_wildcard_1():
    global host
    global port

    # create a client socket
    with grpc.insecure_channel(('{}:{}').format(ip, port)) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        # send the create_account message
        cmd = "show_accounts a*"
        res = "Waiting for a valid response... Please see instructions above."
        # if there is a command prompt, send it and wait for a server response before printing it and continuing
        if len(str.encode(cmd)) > 0:
            if 'create_account' in cmd:
                res = create_account(stub, cmd).response
            if 'log_in' in cmd:
                res = login(stub, cmd).response
            if 'show_accounts' in cmd:
                res = show_accounts(stub, cmd).response
            if 'send_message_to' in cmd:
                res = send_message_to(stub, cmd).response
            if 'delete_account' in cmd:
                res = delete_account(stub, cmd).response
            if 'quit' in cmd:
                res = quit(stub, cmd).response

        # store the response
        assert(res == "bob\nandy\n")

def test_show_accounts_wildcard_2():
    global host
    global port

    # create a client socket
    with grpc.insecure_channel(('{}:{}').format(ip, port)) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        # send the create_account message
        cmd = "show_accounts an*"
        res = "Waiting for a valid response... Please see instructions above."
        # if there is a command prompt, send it and wait for a server response before printing it and continuing
        if len(str.encode(cmd)) > 0:
            if 'create_account' in cmd:
                res = create_account(stub, cmd).response
            if 'log_in' in cmd:
                res = login(stub, cmd).response
            if 'show_accounts' in cmd:
                res = show_accounts(stub, cmd).response
            if 'send_message_to' in cmd:
                res = send_message_to(stub, cmd).response
            if 'delete_account' in cmd:
                res = delete_account(stub, cmd).response
            if 'quit' in cmd:
                res = quit(stub, cmd).response

        # store the response
        assert(res == "andy\n")

def test_show_accounts_wildcard_3():
    global host
    global port

    # create a client socket
    with grpc.insecure_channel(('{}:{}').format(ip, port)) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        # send the create_account message
        cmd = "show_accounts a"
        res = "Waiting for a valid response... Please see instructions above."
        # if there is a command prompt, send it and wait for a server response before printing it and continuing
        if len(str.encode(cmd)) > 0:
            if 'create_account' in cmd:
                res = create_account(stub, cmd).response
            if 'log_in' in cmd:
                res = login(stub, cmd).response
            if 'show_accounts' in cmd:
                res = show_accounts(stub, cmd).response
            if 'send_message_to' in cmd:
                res = send_message_to(stub, cmd).response
            if 'delete_account' in cmd:
                res = delete_account(stub, cmd).response
            if 'quit' in cmd:
                res = quit(stub, cmd).response

        # store the response
        assert(res == "andy\n")

# test create account
def test_send_message_to_valid_account():
    global ip
    global port

    # create a client socket
    with grpc.insecure_channel(('{}:{}').format(ip, port)) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        # send the create_account message
        cmd = "log_in bob"
        res = "Waiting for a valid response... Please see instructions above."
        # if there is a command prompt, send it and wait for a server response before printing it and continuing
        if len(str.encode(cmd)) > 0:
            if 'create_account' in cmd:
                res = create_account(stub, cmd).response
            if 'log_in' in cmd:
                res = login(stub, cmd).response
            if 'show_accounts' in cmd:
                res = show_accounts(stub, cmd).response
            if 'send_message_to' in cmd:
                res = send_message_to(stub, cmd).response
            if 'delete_account' in cmd:
                res = delete_account(stub, cmd).response
            if 'quit' in cmd:
                res = quit(stub, cmd).response

        # send the create_account message
        cmd = "send_message_to andy message: hello andy"
        res = "Waiting for a valid response... Please see instructions above."
        # if there is a command prompt, send it and wait for a server response before printing it and continuing
        if len(str.encode(cmd)) > 0:
            if 'create_account' in cmd:
                res = create_account(stub, cmd).response
            if 'log_in' in cmd:
                res = login(stub, cmd).response
            if 'show_accounts' in cmd:
                res = show_accounts(stub, cmd).response
            if 'send_message_to' in cmd:
                res = send_message_to(stub, cmd).response
            if 'delete_account' in cmd:
                res = delete_account(stub, cmd).response
            if 'quit' in cmd:
                res = quit(stub, cmd).response

        # store the response
        assert(res == "message successfully sent to andy")

def test_send_message_to_non_existent_account():
    global ip
    global port

    # create a client socket
    with grpc.insecure_channel(('{}:{}').format(ip, port)) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        # send the create_account message
        cmd = "log_in bob"
        res = "Waiting for a valid response... Please see instructions above."
        # if there is a command prompt, send it and wait for a server response before printing it and continuing
        if len(str.encode(cmd)) > 0:
            if 'create_account' in cmd:
                res = create_account(stub, cmd).response
            if 'log_in' in cmd:
                res = login(stub, cmd).response
            if 'show_accounts' in cmd:
                res = show_accounts(stub, cmd).response
            if 'send_message_to' in cmd:
                res = send_message_to(stub, cmd).response
            if 'delete_account' in cmd:
                res = delete_account(stub, cmd).response
            if 'quit' in cmd:
                res = quit(stub, cmd).response

        assert(res == "bob is successfully logged in!")

        # send the send_message_to message
        cmd = "send_message_to james message: hello james"
        res = "Waiting for a valid response... Please see instructions above."
        # if there is a command prompt, send it and wait for a server response before printing it and continuing
        if len(str.encode(cmd)) > 0:
            if 'create_account' in cmd:
                res = create_account(stub, cmd).response
            if 'log_in' in cmd:
                res = login(stub, cmd).response
            if 'show_accounts' in cmd:
                res = show_accounts(stub, cmd).response
            if 'send_message_to' in cmd:
                res = send_message_to(stub, cmd).response
            if 'delete_account' in cmd:
                res = delete_account(stub, cmd).response
            if 'quit' in cmd:
                res = quit(stub, cmd).response

        # store the response
        assert(res == "error: the recipient james does not exist, please have them create an account before you can send a message to them")

# test delete account
def test_delete_account():
    global ip
    global port

    # create a client socket
    with grpc.insecure_channel(('{}:{}').format(ip, port)) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        # send the log_in message
        cmd = "log_in bob"
        res = "Waiting for a valid response... Please see instructions above."
        # if there is a command prompt, send it and wait for a server response before printing it and continuing
        if len(str.encode(cmd)) > 0:
            if 'create_account' in cmd:
                res = create_account(stub, cmd).response
            if 'log_in' in cmd:
                res = login(stub, cmd).response
            if 'show_accounts' in cmd:
                res = show_accounts(stub, cmd).response
            if 'send_message_to' in cmd:
                res = send_message_to(stub, cmd).response
            if 'delete_account' in cmd:
                res = delete_account(stub, cmd).response
            if 'quit' in cmd:
                res = quit(stub, cmd).response

        assert(res == "bob is successfully logged in!")

        # send the delete_account message
        cmd = "delete_account bob"
        res = "Waiting for a valid response... Please see instructions above."
        # if there is a command prompt, send it and wait for a server response before printing it and continuing
        if len(str.encode(cmd)) > 0:
            if 'create_account' in cmd:
                res = create_account(stub, cmd).response
            if 'log_in' in cmd:
                res = login(stub, cmd).response
            if 'show_accounts' in cmd:
                res = show_accounts(stub, cmd).response
            if 'send_message_to' in cmd:
                res = send_message_to(stub, cmd).response
            if 'delete_account' in cmd:
                res = delete_account(stub, cmd).response
            if 'quit' in cmd:
                res = quit(stub, cmd).response

        # store the response
        assert(res == "The account bob has been successfully deleted.")

# test show_accounts after delete_account
def test_show_accounts_after_deletion():
    global ip
    global port

    # create a client socket
    with grpc.insecure_channel(('{}:{}').format(ip, port)) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        # send the create_account message
        cmd = "show_accounts"
        res = "Waiting for a valid response... Please see instructions above."
        # if there is a command prompt, send it and wait for a server response before printing it and continuing
        if len(str.encode(cmd)) > 0:
            if 'create_account' in cmd:
                res = create_account(stub, cmd).response
            if 'log_in' in cmd:
                res = login(stub, cmd).response
            if 'show_accounts' in cmd:
                res = show_accounts(stub, cmd).response
            if 'send_message_to' in cmd:
                res = send_message_to(stub, cmd).response
            if 'delete_account' in cmd:
                res = delete_account(stub, cmd).response
            if 'quit' in cmd:
                res = quit(stub, cmd).response

        # store the response
        assert(res == "andy\n")
